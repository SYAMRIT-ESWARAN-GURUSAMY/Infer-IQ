from neo4j import GraphDatabase
import os

class CompetencyGraph:
    def __init__(self, uri=None, auth=None):
        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        auth = auth or (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def seed_initial_ontology(self, questions: list[dict]):
        """Populates concepts, prerequisite relationships, and questions in Neo4j."""
        with self.driver.session() as session:
            for q in questions:
                session.execute_write(self._create_question_and_relations, q)

    @staticmethod
    def _create_question_and_relations(tx, q):
        # Create Question node
        tx.run(
            """
            MERGE (q:Question {id: $id})
            SET q.skill = $skill, q.difficulty = $difficulty, q.rubric = $rubric
            """,
            id=q["id"], skill=q["skill"], difficulty=q["difficulty"], rubric=q["rubric"]
        )
        # Create Concept nodes & relationships
        for concept in q["concepts"]:
            tx.run(
                """
                MERGE (c:Concept {name: $concept})
                MERGE (q:Question {id: $id})
                MERGE (q)-[:TESTS_CONCEPT]->(c)
                """,
                id=q["id"], concept=concept
            )
        # Create Prerequisite relationships
        for prereq in q["prerequisites"]:
            tx.run(
                """
                MERGE (p:Concept {name: $prereq})
                MERGE (q:Question {id: $id})
                MERGE (q)-[:REQUIRES_PREREQ]->(p)
                """,
                id=q["id"], prereq=prereq
            )

    def get_prerequisite_gap(self, question_id: str, candidate_competencies: dict[str, float]) -> float:
        """Traverses graph to calculate average depth requirement score for missing prereqs."""
        query = """
        MATCH (q:Question {id: $qid})-[:REQUIRES_PREREQ]->(p:Concept)
        RETURN p.name AS prereq
        """
        with self.driver.session() as session:
            result = session.run(query, qid=question_id)
            prereqs = [record["prereq"] for record in result]
        
        if not prereqs:
            return 0.0
            
        total_gap = sum(1.0 - candidate_competencies.get(p, 0.35) for p in prereqs)
        return total_gap / len(prereqs)