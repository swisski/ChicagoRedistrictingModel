import random
import networkx as nx
from shapely.ops import unary_union
from copy import deepcopy
import time 
from shapely.ops import unary_union
import numpy as np
from shapely.geometry import Point

def generate_proposal(districts, graph, data, n_districts, max_attempts=10):
    """
    Generate a contiguous redistricting proposal.
    Retries until a valid contiguous proposal is created or max_attempts is reached.
    """
    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1}/{max_attempts}: Generating proposal...")

        new_districts = [list(district) for district in districts]

        # Select a random district
        from_district_idx = random.randint(0, len(new_districts) - 1)
        from_district = new_districts[from_district_idx]
        if not from_district:
            print(f"Attempt {attempt + 1}: Selected district {from_district_idx} is empty. Retrying.")
            continue

        # Identify eligible tracts
        eligible_tracts = []
        for tract in from_district:
            neighbors = list(graph.neighbors(tract))
            external_neighbors = sum(1 for neighbor in neighbors if any(neighbor in d for d in new_districts if d != from_district))
            eligible_tracts.extend([tract] * external_neighbors)

        if not eligible_tracts:
            print(f"Attempt {attempt + 1}: No eligible tracts in district {from_district_idx}. Retrying.")
            continue

        # Select a tract to move
        tract_to_move = random.choice(eligible_tracts)

        # Find neighboring districts
        neighbors = list(graph.neighbors(tract_to_move))
        neighboring_districts = [
            idx for idx, district in enumerate(new_districts)
            if any(neighbor in district for neighbor in neighbors) and idx != from_district_idx
        ]

        if not neighboring_districts:
            print(f"Attempt {attempt + 1}: No neighboring districts for tract {tract_to_move}. Retrying.")
            continue

        # Move the tract
        to_district_idx = random.choice(neighboring_districts)
        from_district.remove(tract_to_move)
        new_districts[to_district_idx].append(tract_to_move)

        # Validate contiguity for both affected districts
        if _is_contiguous(graph, new_districts[from_district_idx]) and _is_contiguous(graph, new_districts[to_district_idx]):
            # Validate the entire districting map
            if all(_is_contiguous(graph, district) for district in new_districts):
                print(f"Attempt {attempt + 1}: Successfully generated a valid proposal.")
                return new_districts

        # Undo the move if validation fails
        print(f"Attempt {attempt + 1}: Validation failed. Reverting changes.")
        new_districts[to_district_idx].remove(tract_to_move)
        from_district.append(tract_to_move)

    print(f"Failed to generate a valid contiguous proposal after {max_attempts} attempts.")
    return None



def _is_contiguous(graph, district):
    """
    Check if a district is contiguous using a subgraph.
    """
    if not district:
        return False
    subgraph = graph.subgraph(district)
    return nx.is_connected(subgraph)


def evaluate_proposal(proposal, data, graph, lodes, n_districts):
    """
    Evaluate a proposal with updated scoring criteria:
    - Compactness: Mean squared distance from district center.
    - Population Parity: Modified standard deviation raised to the fourth power.
    """
    print(f"Started evaluate_proposal at {time.time()}")

    district_centers = []
    compactness_scores = []
    for district in proposal:
        district_data = data[data['tract_code'].isin(district)]
        total_population = district_data['population'].sum()

        if total_population == 0:
            compactness_scores.append(float('inf'))
            continue

        district_data['centroid'] = district_data.geometry.centroid
        x_center = np.average(district_data['centroid'].x, weights=district_data['population'])
        y_center = np.average(district_data['centroid'].y, weights=district_data['population'])
        center = Point(x_center, y_center)
        district_centers.append(center)

        distances = district_data['centroid'].apply(lambda g: g.distance(center))
        mean_squared_distance = np.mean(distances**2)
        compactness_scores.append(mean_squared_distance)

    compactness = -np.mean(compactness_scores)
    print(f"Finished compactness at {time.time()}")


    proposal_tracts = {tract for district in proposal for tract in district}
    filtered_lodes = lodes[
        lodes['workplace_tract_code'].isin(proposal_tracts) |
        lodes['home_tract_code'].isin(proposal_tracts)
    ]
    scores = []
    for district in proposal:
        tracts = set(district)
        district_lodes = filtered_lodes[
            filtered_lodes['workplace_tract_code'].isin(tracts) |
            filtered_lodes['home_tract_code'].isin(tracts)
        ]

        total_live_in_tracts = district_lodes[district_lodes['home_tract_code'].isin(tracts)]['total_jobs'].sum()
        total_work_in_tracts = district_lodes[district_lodes['workplace_tract_code'].isin(tracts)]['total_jobs'].sum()
        live_and_work_in_tracts = district_lodes[
            (district_lodes['workplace_tract_code'].isin(tracts)) &
            (district_lodes['home_tract_code'].isin(tracts))
        ]['total_jobs'].sum()

        percentage_live_and_work = (live_and_work_in_tracts / total_live_in_tracts) * 100 if total_live_in_tracts > 0 else 0
        percentage_work_and_live = (live_and_work_in_tracts / total_work_in_tracts) * 100 if total_work_in_tracts > 0 else 0
        district_score = (2 / 3 * percentage_live_and_work) + (1 / 3 * percentage_work_and_live)
        scores.append(district_score)
    community_preservation = np.mean(scores) / 100
    print(f"Finished LODES at {time.time()}")

    district_populations = np.array([
        data[data['tract_code'].isin(district)]['population'].sum() for district in proposal
    ])
    mean_population = district_populations.mean()
    population_parity = -np.sum((district_populations - mean_population)**4)

    district_hispanic_pop = [
        data[data['tract_code'].isin(district)]['hispanic_latino'].sum() for district in proposal
    ]
    district_black_pop = [
        data[data['tract_code'].isin(district)]['black'].sum() for district in proposal
    ]
    district_total_pop = [
        data[data['tract_code'].isin(district)]['population'].sum() for district in proposal
    ]

    hispanic_majority = sum(1 for h_pop, total_pop in zip(district_hispanic_pop, district_total_pop) if h_pop > total_pop / 2)
    black_majority = sum(1 for b_pop, total_pop in zip(district_black_pop, district_total_pop) if b_pop > total_pop / 2)

    vra_score = 5
    vra_score -= 2 * max(0, 2 - hispanic_majority)
    vra_score -= 2 * max(0, 2 - black_majority)

    total_score = compactness + community_preservation + population_parity + vra_score
    print(
        f"Compactness: {compactness:.4f}, Community Preservation: {community_preservation:.4f}, "
        f"Population Parity: {population_parity:.4f}, VRA Score: {vra_score:.4f}, "
        f"Total Score: {total_score:.4f}"
    )

    return total_score