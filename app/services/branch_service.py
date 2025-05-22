from app.database.mongo import mongo_db

async def create_branch(mongo_client, data):
    collection = mongo_client.chatdb.chat_content
    chat = await collection.find_one({"chat_id": str(data.original_chat_id)})
    if not chat:
        return None
    for pair in chat["qa_pairs"]:
        if pair["response_id"] == data.branch_from_response_id:
            pair["branches"].append(str(data.new_chat_id))
            break
    await collection.update_one({"chat_id": str(data.original_chat_id)}, {"$set": {"qa_pairs": chat["qa_pairs"]}})
    await collection.insert_one({"chat_id": str(data.new_chat_id), "qa_pairs": []})
    return {"chat_id": data.new_chat_id}

async def get_branch_tree(mongo_client, chat_id):
    def build_tree(node):
        chat = tree_map.get(node, [])
        return {"chat_id": node, "children": [build_tree(child) for child in chat]}

    collection = mongo_client.chatdb.chat_content
    cursor = collection.find({})
    tree_map = {}
    async for doc in cursor:
        for qa in doc.get("qa_pairs", []):
            for branch in qa.get("branches", []):
                tree_map.setdefault(doc["chat_id"], []).append(branch)
    return build_tree(str(chat_id))