class ModelNotFound(Exception):
    status_code = 404
    message = "Model not found"
    code = "model_not_found"