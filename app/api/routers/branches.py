from fastapi import APIRouter, Depends
from app.schemas.branch import BranchCreate, BranchTree, SetActiveBranch
from app.services.branch_service import create_branch, get_branch_tree
from app.database.mongo import get_mongo_client
from uuid import UUID

router = APIRouter()

# Endpoint to create a new branch for a chat
@router.post("/create-branch")
async def branch_chat(
    data: BranchCreate,  # Pydantic model with details needed to create a branch
    mongo_client=Depends(get_mongo_client)  # Injected MongoDB client
):
    # Call the service to create a branch in the database
    result = await create_branch(mongo_client, data)
    return result  # Return the result of the branch creation

# Endpoint to fetch the tree structure of all branches for a given chat
@router.get("/get-branches", response_model=BranchTree)
async def fetch_branches(
    chat_id: UUID,  # UUID of the chat for which to fetch branches
    mongo_client=Depends(get_mongo_client)  # Injected MongoDB client
):
    # Call the service to get the branch tree for the specified chat
    return await get_branch_tree(mongo_client, chat_id)

# Endpoint to set a specific branch as active for a given chat
@router.put("/set-active-branch")
async def activate_branch(data: SetActiveBranch):
    # Placeholder: logic for setting the active branch can be implemented,
    # possibly involving updating a record in a SQL database.
    return {"msg": f"Branch {data.branch_id} set as active for chat {data.chat_id}"}