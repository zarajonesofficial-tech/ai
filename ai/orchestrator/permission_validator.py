import json
import os
from typing import List, Optional
import discord

class PermissionValidator:
    ROLE_HIERARCHY = {
        "admin": 3,
        "moderator": 2,
        "user": 1
    }

    def __init__(self):
        self.registry = self._load_registry()

    def _load_registry(self):
        path = os.path.join(os.path.dirname(__file__), "capability_registry.json")
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_user_role_level(self, member: discord.Member) -> int:
        """Determines the highest role level of a Discord member."""
        if hasattr(member, 'guild_permissions') and member.guild_permissions.administrator:
            return self.ROLE_HIERARCHY["admin"]
        
        # Check role names (case-insensitive)
        role_names = [role.name.lower() for role in member.roles]
        
        if any(r in role_names for r in ["admin", "owner", "administrator"]):
            return self.ROLE_HIERARCHY["admin"]
        if any(r in role_names for r in ["moderator", "staff", "mod"]):
            return self.ROLE_HIERARCHY["moderator"]
            
        return self.ROLE_HIERARCHY["user"]

    def can_execute(self, action: str, member: discord.Member) -> bool:
        """Checks if a member has permission to perform a specific action."""
        required_role = self.registry.get(action)
        if not required_role:
            return False # Action not in registry
            
        required_level = self.ROLE_HIERARCHY.get(required_role, 1)
        user_level = self.get_user_role_level(member)
        
        return user_level >= required_level

permission_validator = PermissionValidator()
