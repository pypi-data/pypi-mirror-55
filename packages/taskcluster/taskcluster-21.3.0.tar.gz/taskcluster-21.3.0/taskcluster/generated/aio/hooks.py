# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from ...aio.asyncclient import AsyncBaseClient
from ...aio.asyncclient import createApiClient
from ...aio.asyncclient import config
from ...aio.asyncclient import createTemporaryCredentials
from ...aio.asyncclient import createSession
_defaultConfig = config


class Hooks(AsyncBaseClient):
    """
    The hooks service provides a mechanism for creating tasks in response to events.

    """

    classOptions = {
    }
    serviceName = 'hooks'
    apiVersion = 'v1'

    async def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    async def listHookGroups(self, *args, **kwargs):
        """
        List hook groups

        This endpoint will return a list of all hook groups with at least one hook.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listHookGroups"], *args, **kwargs)

    async def listHooks(self, *args, **kwargs):
        """
        List hooks in a given group

        This endpoint will return a list of all the hook definitions within a
        given hook group.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listHooks"], *args, **kwargs)

    async def hook(self, *args, **kwargs):
        """
        Get hook definition

        This endpoint will return the hook definition for the given `hookGroupId`
        and hookId.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["hook"], *args, **kwargs)

    async def getHookStatus(self, *args, **kwargs):
        """
        Get hook status

        This endpoint will return the current status of the hook.  This represents a
        snapshot in time and may vary from one call to the next.

        This method is deprecated in favor of listLastFires.

        This method is ``deprecated``
        """

        return await self._makeApiCall(self.funcinfo["getHookStatus"], *args, **kwargs)

    async def createHook(self, *args, **kwargs):
        """
        Create a hook

        This endpoint will create a new hook.

        The caller's credentials must include the role that will be used to
        create the task.  That role must satisfy task.scopes as well as the
        necessary scopes to add the task to the queue.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createHook"], *args, **kwargs)

    async def updateHook(self, *args, **kwargs):
        """
        Update a hook

        This endpoint will update an existing hook.  All fields except
        `hookGroupId` and `hookId` can be modified.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["updateHook"], *args, **kwargs)

    async def removeHook(self, *args, **kwargs):
        """
        Delete a hook

        This endpoint will remove a hook definition.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["removeHook"], *args, **kwargs)

    async def triggerHook(self, *args, **kwargs):
        """
        Trigger a hook

        This endpoint will trigger the creation of a task from a hook definition.

        The HTTP payload must match the hooks `triggerSchema`.  If it does, it is
        provided as the `payload` property of the JSON-e context used to render the
        task template.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["triggerHook"], *args, **kwargs)

    async def getTriggerToken(self, *args, **kwargs):
        """
        Get a trigger token

        Retrieve a unique secret token for triggering the specified hook. This
        token can be deactivated with `resetTriggerToken`.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["getTriggerToken"], *args, **kwargs)

    async def resetTriggerToken(self, *args, **kwargs):
        """
        Reset a trigger token

        Reset the token for triggering a given hook. This invalidates token that
        may have been issued via getTriggerToken with a new token.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["resetTriggerToken"], *args, **kwargs)

    async def triggerHookWithToken(self, *args, **kwargs):
        """
        Trigger a hook with a token

        This endpoint triggers a defined hook with a valid token.

        The HTTP payload must match the hooks `triggerSchema`.  If it does, it is
        provided as the `payload` property of the JSON-e context used to render the
        task template.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["triggerHookWithToken"], *args, **kwargs)

    async def listLastFires(self, *args, **kwargs):
        """
        Get information about recent hook fires

        This endpoint will return information about the the last few times this hook has been
        fired, including whether the hook was fired successfully or not

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["listLastFires"], *args, **kwargs)

    funcinfo = {
        "createHook": {
            'args': ['hookGroupId', 'hookId'],
            'input': 'v1/create-hook-request.json#',
            'method': 'put',
            'name': 'createHook',
            'output': 'v1/hook-definition.json#',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'stable',
        },
        "getHookStatus": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'getHookStatus',
            'output': 'v1/hook-status.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/status',
            'stability': 'deprecated',
        },
        "getTriggerToken": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'getTriggerToken',
            'output': 'v1/trigger-token-response.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/token',
            'stability': 'stable',
        },
        "hook": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'hook',
            'output': 'v1/hook-definition.json#',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'stable',
        },
        "listHookGroups": {
            'args': [],
            'method': 'get',
            'name': 'listHookGroups',
            'output': 'v1/list-hook-groups-response.json#',
            'route': '/hooks',
            'stability': 'stable',
        },
        "listHooks": {
            'args': ['hookGroupId'],
            'method': 'get',
            'name': 'listHooks',
            'output': 'v1/list-hooks-response.json#',
            'route': '/hooks/<hookGroupId>',
            'stability': 'stable',
        },
        "listLastFires": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'get',
            'name': 'listLastFires',
            'output': 'v1/list-lastFires-response.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/last-fires',
            'stability': 'experimental',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
        "removeHook": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'delete',
            'name': 'removeHook',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'stable',
        },
        "resetTriggerToken": {
            'args': ['hookGroupId', 'hookId'],
            'method': 'post',
            'name': 'resetTriggerToken',
            'output': 'v1/trigger-token-response.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/token',
            'stability': 'stable',
        },
        "triggerHook": {
            'args': ['hookGroupId', 'hookId'],
            'input': 'v1/trigger-hook.json#',
            'method': 'post',
            'name': 'triggerHook',
            'output': 'v1/trigger-hook-response.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/trigger',
            'stability': 'stable',
        },
        "triggerHookWithToken": {
            'args': ['hookGroupId', 'hookId', 'token'],
            'input': 'v1/trigger-hook.json#',
            'method': 'post',
            'name': 'triggerHookWithToken',
            'output': 'v1/trigger-hook-response.json#',
            'route': '/hooks/<hookGroupId>/<hookId>/trigger/<token>',
            'stability': 'stable',
        },
        "updateHook": {
            'args': ['hookGroupId', 'hookId'],
            'input': 'v1/create-hook-request.json#',
            'method': 'post',
            'name': 'updateHook',
            'output': 'v1/hook-definition.json#',
            'route': '/hooks/<hookGroupId>/<hookId>',
            'stability': 'stable',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Hooks']
