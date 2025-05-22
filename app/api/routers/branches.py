from fastapi import APIRouter, Depends
from app.schemas.branch import BranchCreate, BranchTree, SetActiveBranch
from app.services.branch_service import create_branch, get_branch_tree
from app.database.mongo import get_mongo_client
from uuid import UUID

router = APIRouter()

@router.post("/create-branch")
async def branch_chat(data: BranchCreate, mongo_client = Depends(get_mongo_client)):
    result = await create_branch(mongo_client, data)
    return result

@router.get("/get-branches", response_model=BranchTree)
async def fetch_branches(chat_id: UUID, mongo_client = Depends(get_mongo_client)):
    return await get_branch_tree(mongo_client, chat_id)

@router.put("/set-active-branch")
async def activate_branch(data: SetActiveBranch):
    # This logic could involve setting the active branch in SQL
    return {"msg": f"Branch {data.branch_id} set as active for chat {data.chat_id}"}