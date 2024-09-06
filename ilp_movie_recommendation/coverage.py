# Import required classes from your ILP system
from andante.logic_concepts import Clause, Goal
from andante.knowledge import Knowledge
from andante.solver import AndanteSolver

def evaluate_clause_coverage(clause, positive_examples, negative_examples, background_knowledge, m=5, p_0=0.5):
    """
    Evaluate the coverage of a clause against positive and negative examples.    Parameters:
    - clause (Clause): The clause to evaluate.
    - positive_examples (list of Clause): List of positive examples to test.
    - negative_examples (list of Clause): List of negative examples to test.
    - background_knowledge (Knowledge): Background knowledge to utilize during evaluation.
    - m (int): Smoothing parameter for the m-estimate calculation.
    - p_0 (float): Prior estimate of the proportion of positive examples.
    Returns:
    - dict: A dictionary containing the coverage information:
      - "positive_entailed": Number of positive examples entailed by the clause.
      - "positive_not_entailed": Number of positive examples not entailed by the clause.
      - "negative_entailed": Number of negative examples entailed by the clause.
      - "negative_not_entailed": Number of negative examples not entailed by the clause.
      - "score": The calculated \(P - N\) score.
      - "m_estimate": The calculated m-estimate.
    """
    assert isinstance(clause, Clause), "The clause parameter must be an instance of Clause"
    assert isinstance(background_knowledge, Knowledge), "The background_knowledge parameter must be an instance of Knowledge"    
    # Initialize counts for the results
    positive_entailed = 0
    positive_not_entailed = 0
    negative_entailed = 0
    negative_not_entailed = 0  
    # Initialize the solver
    solver = AndanteSolver()   
    background_knowledge.add(clause) 
    # Check positive examples
    for example in positive_examples:
        goal = Goal([example.head])  # Wrap example head in a Goal
        is_entailed = solver.succeeds_on(goal, background_knowledge)
        if is_entailed:
            positive_entailed += 1
        else:
            positive_not_entailed += 1    
    # Check negative examples
    for example in negative_examples:
        goal = Goal([example.head])  # Wrap example head in a Goal
        is_entailed = solver.succeeds_on(goal, background_knowledge)
        if is_entailed:
            negative_entailed += 1
        else:
            negative_not_entailed += 1    
    # Calculate the \(P - N\) score
    score = positive_entailed - negative_entailed    
    # Calculate the m-estimate
    total_covered = positive_entailed + negative_entailed
    m_estimate = (positive_entailed + m * p_0) / (total_covered + m) if total_covered > 0 else 0    
    # Display the results
    """ print(f"Positive examples entailed: {positive_entailed}")
    print(f"Positive examples not entailed: {positive_not_entailed}")
    print(f"Negative examples entailed: {negative_entailed}")
    print(f"Negative examples not entailed: {negative_not_entailed}")
    print(f"Coverage score (P - N): {score}")
    print(f"m-estimate: {m_estimate}")     """
    return {
        "positive_entailed": positive_entailed,
        "positive_not_entailed": positive_not_entailed,
        "negative_entailed": negative_entailed,
        "negative_not_entailed": negative_not_entailed,
        "score": score,
        "m_estimate": m_estimate,
    }