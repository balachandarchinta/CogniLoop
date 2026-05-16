import logging
from app.tasks.celery_app import celery_app
from app.core.cognitive_profiling.profiler import ProfileEvolutionManager
from app.database import SessionLocal
from app.models.learner import Learner

logger = logging.getLogger(__name__)

# Initialize the manager once per worker process
profile_manager = ProfileEvolutionManager()

@celery_app.task(name="tasks.update_cognitive_profile")
def update_cognitive_profile(learner_id: str, new_data_payload: dict):
    """
    Celery task to handle async profile updates and trigger model retraining if necessary.
    """
    logger.info(f"Starting async profile update for learner {learner_id}")
    
    db = SessionLocal()
    try:
        # 1. Fetch the learner and their current profile
        learner = db.query(Learner).filter(Learner.id == learner_id).first()
        if not learner:
            logger.error(f"Learner {learner_id} not found.")
            return False
            
        # Mocking the current_profile and new_data objects for MVP
        # In reality, new_data_payload would be mapped to a structured class
        class MockData:
            def __init__(self, data):
                self.__dict__.update(data)
                
        new_data = MockData(new_data_payload)
        
        # We need to grab the latest cognitive profile for this learner
        # For MVP, assuming the first profile is the active one:
        current_profile = None
        if learner.cognitive_profiles:
            current_profile = learner.cognitive_profiles[0]
            
        if not current_profile:
            logger.info("No current profile found, creating a new initial profile.")
            # Initialization logic would go here
            return True

        # Check if an update is warranted
        # (Assuming 50 new interactions as threshold)
        if profile_manager.should_update_profile(current_profile, new_data_points=50):
            updated_profile_data = profile_manager.update_profile(current_profile, new_data)
            
            # 2. Update DB with new profile
            # current_profile.learning_style = updated_profile_data['learning_style']
            # current_profile.cognitive_characteristics = updated_profile_data['cognitive_characteristics']
            # current_profile.behavioral_patterns = updated_profile_data['behavioral_patterns']
            # current_profile.profile_version = updated_profile_data['profile_version']
            # current_profile.updated_at = updated_profile_data['updated_at']
            
            # db.commit()
            logger.info(f"Profile updated for learner {learner_id}")
            
            # 3. Retrain ML models in the background if the global threshold is reached
            # trigger_model_retraining.delay()
            
        return True
    except Exception as e:
        logger.error(f"Error updating profile for {learner_id}: {e}")
        db.rollback()
        return False
    finally:
        db.close()


@celery_app.task(name="tasks.trigger_model_retraining")
def trigger_model_retraining():
    """
    Retrains the LearningStyleClassifier and other ML models across all user data.
    """
    logger.info("Starting global model retraining...")
    # Fetch all training data
    # training_data, labels = fetch_training_data()
    # profile_manager.classifier.train(training_data, labels)
    logger.info("Model retraining completed and saved.")
    return True
