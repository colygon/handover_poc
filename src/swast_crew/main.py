#!/usr/bin/env python
"""
SWAST Healthcare Analytics - Main Entry Point
Run the healthcare analytics crew for hospital handover analysis
"""
import sys
from .crew import SWASTCrew


def run():
    """
    Run the SWAST Healthcare Analytics crew
    """
    print("=" * 60)
    print("SWAST Healthcare Analytics Crew")
    print("Analyzing Hospital Handover Delays")
    print("=" * 60)

    # Get hospital name from command line or use default
    hospital_name = sys.argv[1] if len(sys.argv) > 1 else "All"

    print(f"\nAnalyzing data for: {hospital_name}")
    print("-" * 60)

    # Initialize and run the crew
    inputs = {
        'hospital_name': hospital_name
    }

    swast_crew = SWASTCrew()
    result = swast_crew.crew().kickoff(inputs=inputs)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(result)

    return result


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'hospital_name': 'All'
    }
    try:
        SWASTCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SWASTCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        'hospital_name': 'All'
    }
    try:
        SWASTCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
