"""Upgrade DB"""
from pymongo import MongoClient

from app.core.settings import settings

# Conectate a tu base de datos
# Cambiá esto si usás otro host/puerto
client = MongoClient(settings.mongo.MONGO_URL)
db = client[settings.mongo.MONGO_DATABASE]
collection = db["writings"]

# # Filtrá los documentos que tienen el campo antiguo
# query = {"student_response_image_url": {"$exists": True}}

# # Opcional: mostrar cuántos documentos van a ser modificados
# count = collection.count_documents(query)
# print(f"Documentos a actualizar: {count}")

# # Iterá por cada documento y hacé el update
# for doc in collection.find(query):
#     old_url = doc.get("student_response_image_url")

#     if old_url:
#         collection.update_one(
#             {"_id": doc["_id"]},
#             {
#                 "$set": {"student_response_image_urls": [old_url]},
#                 "$unset": {"student_response_image_url": ""}
#             }
#         )


# Itera sobre todos los documentos en la colección
for doc in collection.find():
    updates = {}
    # Verifica y convierte 'writing_score' si es un entero
    if isinstance(doc.get("writing_score"), int):
        updates["writing_score"] = float(doc["writing_score"])

    # Verifica y convierte cada 'score' en 'ai_feedback.criteria_scores' si es un entero
    criteria_scores = doc.get("ai_feedback", {}).get("criterias", [])
    updated_scores = []
    MODIFIED = False
    for score_entry in criteria_scores:
        if isinstance(score_entry.get("score"), int):
            score_entry["score"] = float(score_entry["score"])
            MODIFIED = True
        updated_scores.append(score_entry)

    if MODIFIED:
        updates["ai_feedback.criterias"] = updated_scores

    # Aplica las actualizaciones si hay cambios
    if updates:
        collection.update_one({"_id": doc["_id"]}, {"$set": updates})

print("Actualización completa.")
