import json
from app.database.prisma import prisma
from app.utils.constants import DICT_TYPES

async def load_dictionaries_from_file(file_path: str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)  # Assumes JSON format: {"type_name": [{"value": "val", "probability": float}, ...]}
        
        for type_name in DICT_TYPES:
            type_data = await prisma.dictionarytype.find_unique(where={"name": type_name})
            if not type_data:
                type_data = await prisma.dictionarytype.create(data={"name": type_name})
            
            items = data.get(type_name, [])
            for item in items:
                existing = await prisma.dictionaryitem.find_first(
                    where={"type_id": type_data.id, "value": item["value"]}
                )
                if not existing:
                    await prisma.dictionaryitem.create(
                        data={
                            "type_id": type_data.id,
                            "value": item["value"],
                            "probability": item.get("probability")
                        }
                    )
    except Exception as e:
        raise Exception(f"Failed to load dictionaries: {str(e)}")