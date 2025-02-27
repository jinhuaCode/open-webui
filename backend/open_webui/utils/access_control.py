from typing import Optional, Union, List, Dict, Any
from open_webui.models.users import Users, UserModel
from open_webui.models.groups import Groups
<<<<<<< HEAD


from open_webui.config import DEFAULT_USER_PERMISSIONS
import json


def fill_missing_permissions(
    permissions: Dict[str, Any], default_permissions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Recursively fills in missing properties in the permissions dictionary
    using the default permissions as a template.
    """
    for key, value in default_permissions.items():
        if key not in permissions:
            permissions[key] = value
        elif isinstance(value, dict) and isinstance(
            permissions[key], dict
        ):  # Both are nested dictionaries
            permissions[key] = fill_missing_permissions(permissions[key], value)

    return permissions


=======
import json


>>>>>>> dfef03c8e (同步远程)
def get_permissions(
    user_id: str,
    default_permissions: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Get all permissions for a user by combining the permissions of all groups the user is a member of.
    If a permission is defined in multiple groups, the most permissive value is used (True > False).
    Permissions are nested in a dict with the permission key as the key and a boolean as the value.
    """

    def combine_permissions(
        permissions: Dict[str, Any], group_permissions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine permissions from multiple groups by taking the most permissive value."""
        for key, value in group_permissions.items():
            if isinstance(value, dict):
                if key not in permissions:
                    permissions[key] = {}
                permissions[key] = combine_permissions(permissions[key], value)
            else:
                if key not in permissions:
                    permissions[key] = value
                else:
<<<<<<< HEAD
                    permissions[key] = (
                        permissions[key] or value
                    )  # Use the most permissive value (True > False)
=======
                    permissions[key] = permissions[key] or value
>>>>>>> dfef03c8e (同步远程)
        return permissions

    user_groups = Groups.get_groups_by_member_id(user_id)

<<<<<<< HEAD
    # Deep copy default permissions to avoid modifying the original dict
    permissions = json.loads(json.dumps(default_permissions))

    # Combine permissions from all user groups
=======
    # deep copy default permissions to avoid modifying the original dict
    permissions = json.loads(json.dumps(default_permissions))

>>>>>>> dfef03c8e (同步远程)
    for group in user_groups:
        group_permissions = group.permissions
        permissions = combine_permissions(permissions, group_permissions)

<<<<<<< HEAD
    # Ensure all fields from default_permissions are present and filled in
    permissions = fill_missing_permissions(permissions, default_permissions)

=======
>>>>>>> dfef03c8e (同步远程)
    return permissions


def has_permission(
    user_id: str,
    permission_key: str,
<<<<<<< HEAD
    default_permissions: Dict[str, Any] = {},
) -> bool:
    """
    Check if a user has a specific permission by checking the group permissions
    and fall back to default permissions if not found in any group.
=======
    default_permissions: Dict[str, bool] = {},
) -> bool:
    """
    Check if a user has a specific permission by checking the group permissions
    and falls back to default permissions if not found in any group.
>>>>>>> dfef03c8e (同步远程)

    Permission keys can be hierarchical and separated by dots ('.').
    """

<<<<<<< HEAD
    def get_permission(permissions: Dict[str, Any], keys: List[str]) -> bool:
=======
    def get_permission(permissions: Dict[str, bool], keys: List[str]) -> bool:
>>>>>>> dfef03c8e (同步远程)
        """Traverse permissions dict using a list of keys (from dot-split permission_key)."""
        for key in keys:
            if key not in permissions:
                return False  # If any part of the hierarchy is missing, deny access
<<<<<<< HEAD
            permissions = permissions[key]  # Traverse one level deeper
=======
            permissions = permissions[key]  # Go one level deeper
>>>>>>> dfef03c8e (同步远程)

        return bool(permissions)  # Return the boolean at the final level

    permission_hierarchy = permission_key.split(".")

    # Retrieve user group permissions
    user_groups = Groups.get_groups_by_member_id(user_id)

    for group in user_groups:
        group_permissions = group.permissions
        if get_permission(group_permissions, permission_hierarchy):
            return True

<<<<<<< HEAD
    # Check default permissions afterward if the group permissions don't allow it
    default_permissions = fill_missing_permissions(
        default_permissions, DEFAULT_USER_PERMISSIONS
    )
=======
    # Check default permissions afterwards if the group permissions don't allow it
>>>>>>> dfef03c8e (同步远程)
    return get_permission(default_permissions, permission_hierarchy)


def has_access(
    user_id: str,
    type: str = "write",
    access_control: Optional[dict] = None,
) -> bool:
    if access_control is None:
        return type == "read"

    user_groups = Groups.get_groups_by_member_id(user_id)
    user_group_ids = [group.id for group in user_groups]
    permission_access = access_control.get(type, {})
    permitted_group_ids = permission_access.get("group_ids", [])
    permitted_user_ids = permission_access.get("user_ids", [])

    return user_id in permitted_user_ids or any(
        group_id in permitted_group_ids for group_id in user_group_ids
    )


# Get all users with access to a resource
def get_users_with_access(
    type: str = "write", access_control: Optional[dict] = None
) -> List[UserModel]:
    if access_control is None:
        return Users.get_users()

    permission_access = access_control.get(type, {})
    permitted_group_ids = permission_access.get("group_ids", [])
    permitted_user_ids = permission_access.get("user_ids", [])

    user_ids_with_access = set(permitted_user_ids)

    for group_id in permitted_group_ids:
        group_user_ids = Groups.get_group_user_ids_by_id(group_id)
        if group_user_ids:
            user_ids_with_access.update(group_user_ids)

    return Users.get_users_by_user_ids(list(user_ids_with_access))
