"""
    Copyright 2019 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime

import pytest

from inmanta import config, const, data, loader, resources
from inmanta.agent import handler
from inmanta.agent.agent import Agent
from inmanta.export import upload_code
from inmanta.protocol import Client
from inmanta.server import SLICE_AGENT_MANAGER, SLICE_ORCHESTRATION, SLICE_RESOURCE, SLICE_SERVER, SLICE_SESSION_MANAGER
from inmanta.server import config as opt
from inmanta.server.bootloader import InmantaBootloader
from inmanta.util import get_compiler_version, hash_file
from utils import log_contains, log_doesnt_contain, retry_limited

LOGGER = logging.getLogger(__name__)


@pytest.mark.asyncio(timeout=60)
@pytest.mark.slowtest
async def test_autostart(server, client, environment, caplog):
    """
        Test auto start of agent
    """
    env = await data.Environment.get_by_id(uuid.UUID(environment))
    await env.set(data.AUTOSTART_AGENT_MAP, {"iaas_agent": "", "iaas_agentx": ""})

    agentmanager = server.get_slice(SLICE_AGENT_MANAGER)
    sessionendpoint = server.get_slice(SLICE_SESSION_MANAGER)

    await agentmanager.ensure_agent_registered(env, "iaas_agent")
    await agentmanager.ensure_agent_registered(env, "iaas_agentx")

    res = await agentmanager._ensure_agents(env, ["iaas_agent"])
    assert res

    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 20)
    assert len(sessionendpoint._sessions) == 1
    res = await agentmanager._ensure_agents(env, ["iaas_agent"])
    assert not res
    assert len(sessionendpoint._sessions) == 1

    LOGGER.warning("Killing agent")
    agentmanager._agent_procs[env.id].proc.terminate()
    await agentmanager._agent_procs[env.id].wait_for_exit(raise_error=False)
    await retry_limited(lambda: len(sessionendpoint._sessions) == 0, 20)
    # Prevent race condition
    await retry_limited(lambda: len(agentmanager.tid_endpoint_to_session) == 0, 20)
    res = await agentmanager._ensure_agents(env, ["iaas_agent"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 3)
    assert len(sessionendpoint._sessions) == 1

    # second agent for same env
    res = await agentmanager._ensure_agents(env, ["iaas_agentx"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 20)
    assert len(sessionendpoint._sessions) == 1

    # Test stopping all agents
    await agentmanager.stop_agents(env)
    assert len(sessionendpoint._sessions) == 0
    assert len(agentmanager._agent_procs) == 0

    log_doesnt_contain(caplog, "inmanta.config", logging.WARNING, "rest_transport not defined")


@pytest.mark.asyncio(timeout=60)
@pytest.mark.slowtest
async def test_autostart_dual_env(client, server):
    """
        Test auto start of agent
    """
    agentmanager = server.get_slice(SLICE_AGENT_MANAGER)
    sessionendpoint = server.get_slice(SLICE_SESSION_MANAGER)

    result = await client.create_project("env-test")
    assert result.code == 200
    project_id = result.result["project"]["id"]

    result = await client.create_environment(project_id=project_id, name="dev")
    env_id = result.result["environment"]["id"]

    result = await client.create_environment(project_id=project_id, name="devx")
    env_id2 = result.result["environment"]["id"]

    env = await data.Environment.get_by_id(uuid.UUID(env_id))
    await env.set(data.AUTOSTART_AGENT_MAP, {"iaas_agent": ""})

    env2 = await data.Environment.get_by_id(uuid.UUID(env_id2))
    await env2.set(data.AUTOSTART_AGENT_MAP, {"iaas_agent": ""})

    await agentmanager.ensure_agent_registered(env, "iaas_agent")
    await agentmanager.ensure_agent_registered(env2, "iaas_agent")

    res = await agentmanager._ensure_agents(env, ["iaas_agent"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 20)
    assert len(sessionendpoint._sessions) == 1

    res = await agentmanager._ensure_agents(env2, ["iaas_agent"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 2, 20)
    assert len(sessionendpoint._sessions) == 2


@pytest.mark.asyncio(timeout=60)
@pytest.mark.slowtest
async def test_autostart_batched(client, server, environment):
    """
        Test auto start of agent
    """
    env = await data.Environment.get_by_id(uuid.UUID(environment))
    await env.set(data.AUTOSTART_AGENT_MAP, {"iaas_agent": "", "iaas_agentx": ""})

    agentmanager = server.get_slice(SLICE_AGENT_MANAGER)
    sessionendpoint = server.get_slice(SLICE_SESSION_MANAGER)

    await agentmanager.ensure_agent_registered(env, "iaas_agent")
    await agentmanager.ensure_agent_registered(env, "iaas_agentx")

    res = await agentmanager._ensure_agents(env, ["iaas_agent", "iaas_agentx"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 20)
    assert len(sessionendpoint._sessions) == 1
    res = await agentmanager._ensure_agents(env, ["iaas_agent"])
    assert not res
    assert len(sessionendpoint._sessions) == 1

    res = await agentmanager._ensure_agents(env, ["iaas_agent", "iaas_agentx"])
    assert not res
    assert len(sessionendpoint._sessions) == 1

    LOGGER.warning("Killing agent")
    agentmanager._agent_procs[env.id].proc.terminate()
    await agentmanager._agent_procs[env.id].wait_for_exit(raise_error=False)
    await retry_limited(lambda: len(sessionendpoint._sessions) == 0, 20)
    # Prevent race condition
    await retry_limited(lambda: len(agentmanager.tid_endpoint_to_session) == 0, 20)
    res = await agentmanager._ensure_agents(env, ["iaas_agent", "iaas_agentx"])
    assert res
    await retry_limited(lambda: len(sessionendpoint._sessions) == 1, 3)
    assert len(sessionendpoint._sessions) == 1


@pytest.mark.asyncio(timeout=10)
async def test_version_removal(client, server):
    """
        Test auto removal of older deploy model versions
    """
    result = await client.create_project("env-test")
    assert result.code == 200
    project_id = result.result["project"]["id"]

    result = await client.create_environment(project_id=project_id, name="dev")
    env_id = result.result["environment"]["id"]

    for _i in range(20):
        version = (await client.reserve_version(env_id)).result["data"]

        await server.get_slice(SLICE_ORCHESTRATION)._purge_versions()
        res = await client.put_version(
            tid=env_id, version=version, resources=[], unknowns=[], version_info={}, compiler_version=get_compiler_version()
        )
        assert res.code == 200
        result = await client.get_project(id=project_id)

        versions = await client.list_versions(tid=env_id)
        assert versions.result["count"] <= opt.server_version_to_keep.get() + 1


@pytest.mark.asyncio(timeout=30)
@pytest.mark.slowtest
async def test_get_resource_for_agent(server_multi, client_multi, environment_multi):
    """
        Test the server to manage the updates on a model during agent deploy
    """
    agent = Agent("localhost", {"nvblah": "localhost"}, environment=environment_multi, code_loader=False)
    agent.add_end_point_name("vm1.dev.inmanta.com")
    agent.add_end_point_name("vm2.dev.inmanta.com")
    await agent.start()
    aclient = agent._client

    version = (await client_multi.reserve_version(environment_multi)).result["data"]

    resources = [
        {
            "group": "root",
            "hash": "89bf880a0dc5ffc1156c8d958b4960971370ee6a",
            "id": "std::File[vm1.dev.inmanta.com,path=/etc/sysconfig/network],v=%d" % version,
            "owner": "root",
            "path": "/etc/sysconfig/network",
            "permissions": 644,
            "purged": False,
            "reload": False,
            "requires": [],
            "version": version,
        },
        {
            "group": "root",
            "hash": "b4350bef50c3ec3ee532d4a3f9d6daedec3d2aba",
            "id": "std::File[vm2.dev.inmanta.com,path=/etc/motd],v=%d" % version,
            "owner": "root",
            "path": "/etc/motd",
            "permissions": 644,
            "purged": False,
            "reload": False,
            "requires": [],
            "version": version,
        },
        {
            "group": "root",
            "hash": "3bfcdad9ab7f9d916a954f1a96b28d31d95593e4",
            "id": "std::File[vm1.dev.inmanta.com,path=/etc/hostname],v=%d" % version,
            "owner": "root",
            "path": "/etc/hostname",
            "permissions": 644,
            "purged": False,
            "reload": False,
            "requires": [],
            "version": version,
        },
        {
            "id": "std::Service[vm1.dev.inmanta.com,name=network],v=%d" % version,
            "name": "network",
            "onboot": True,
            "requires": ["std::File[vm1.dev.inmanta.com,path=/etc/sysconfig/network],v=%d" % version],
            "state": "running",
            "version": version,
        },
    ]

    res = await client_multi.put_version(
        tid=environment_multi,
        version=version,
        resources=resources,
        unknowns=[],
        version_info={},
        compiler_version=get_compiler_version(),
    )
    assert res.code == 200

    result = await client_multi.list_versions(environment_multi)
    assert result.code == 200
    assert result.result["count"] == 1

    result = await client_multi.release_version(environment_multi, version, False)
    assert result.code == 200

    result = await client_multi.get_version(environment_multi, version)
    assert result.code == 200
    assert result.result["model"]["version"] == version
    assert result.result["model"]["total"] == len(resources)
    assert result.result["model"]["released"]
    assert result.result["model"]["result"] == "deploying"

    result = await aclient.get_resources_for_agent(environment_multi, "vm1.dev.inmanta.com")
    assert result.code == 200
    assert len(result.result["resources"]) == 3

    action_id = uuid.uuid4()
    now = datetime.now()
    result = await aclient.resource_action_update(
        environment_multi,
        ["std::File[vm1.dev.inmanta.com,path=/etc/sysconfig/network],v=%d" % version],
        action_id,
        "deploy",
        now,
        now,
        "deployed",
        [],
        {},
    )

    assert result.code == 200

    result = await client_multi.get_version(environment_multi, version)
    assert result.code == 200
    assert result.result["model"]["done"] == 1

    action_id = uuid.uuid4()
    now = datetime.now()
    result = await aclient.resource_action_update(
        environment_multi,
        ["std::File[vm1.dev.inmanta.com,path=/etc/hostname],v=%d" % version],
        action_id,
        "deploy",
        now,
        now,
        "deployed",
        [],
        {},
    )
    assert result.code == 200

    result = await client_multi.get_version(environment_multi, version)
    assert result.code == 200
    assert result.result["model"]["done"] == 2
    await agent.stop()


@pytest.mark.asyncio(timeout=10)
async def test_get_environment(client, clienthelper, server, environment):
    for i in range(10):
        version = await clienthelper.get_version()

        resources = []
        for j in range(i):
            resources.append(
                {
                    "group": "root",
                    "hash": "89bf880a0dc5ffc1156c8d958b4960971370ee6a",
                    "id": "std::File[vm1.dev.inmanta.com,path=/tmp/file%d],v=%d" % (j, version),
                    "owner": "root",
                    "path": "/tmp/file%d" % j,
                    "permissions": 644,
                    "purged": False,
                    "reload": False,
                    "requires": [],
                    "version": version,
                }
            )

        res = await client.put_version(
            tid=environment,
            version=version,
            resources=resources,
            unknowns=[],
            version_info={},
            compiler_version=get_compiler_version(),
        )
        assert res.code == 200

    result = await client.get_environment(environment, versions=5, resources=1)
    assert result.code == 200
    assert len(result.result["environment"]["versions"]) == 5
    assert len(result.result["environment"]["resources"]) == 9


@pytest.mark.asyncio
async def test_resource_update(postgresql_client, client, clienthelper, server, environment):
    """
        Test updating resources and logging
    """
    agent = Agent("localhost", {"blah": "localhost"}, environment=environment, code_loader=False)
    await agent.start()
    aclient = agent._client

    version = await clienthelper.get_version()

    resources = []
    for j in range(10):
        resources.append(
            {
                "group": "root",
                "hash": "89bf880a0dc5ffc1156c8d958b4960971370ee6a",
                "id": "std::File[vm1,path=/tmp/file%d],v=%d" % (j, version),
                "owner": "root",
                "path": "/tmp/file%d" % j,
                "permissions": 644,
                "purged": False,
                "reload": False,
                "requires": [],
                "version": version,
            }
        )

    res = await client.put_version(
        tid=environment,
        version=version,
        resources=resources,
        unknowns=[],
        version_info={},
        compiler_version=get_compiler_version(),
    )
    assert res.code == 200

    result = await client.release_version(environment, version, False)
    assert result.code == 200

    resource_ids = [x["id"] for x in resources]

    # Start the deploy
    action_id = uuid.uuid4()
    now = datetime.now()
    result = await aclient.resource_action_update(
        environment, resource_ids, action_id, "deploy", now, status=const.ResourceState.deploying
    )
    assert result.code == 200

    # Get the status from a resource
    result = await client.get_resource(tid=environment, id=resource_ids[0], logs=True)
    assert result.code == 200
    logs = {x["action"]: x for x in result.result["logs"]}

    assert "deploy" in logs
    assert "finished" not in logs["deploy"]
    assert "messages" not in logs["deploy"]
    assert "changes" not in logs["deploy"]

    # Send some logs
    result = await aclient.resource_action_update(
        environment,
        resource_ids,
        action_id,
        "deploy",
        status=const.ResourceState.deploying,
        messages=[data.LogLine.log(const.LogLevel.INFO, "Test log %(a)s %(b)s", a="a", b="b")],
    )
    assert result.code == 200

    # Get the status from a resource
    result = await client.get_resource(tid=environment, id=resource_ids[0], logs=True)
    assert result.code == 200
    logs = {x["action"]: x for x in result.result["logs"]}

    assert "deploy" in logs
    assert "messages" in logs["deploy"]
    assert len(logs["deploy"]["messages"]) == 1
    assert logs["deploy"]["messages"][0]["msg"] == "Test log a b"
    assert "finished" not in logs["deploy"]
    assert "changes" not in logs["deploy"]

    # Finish the deploy
    now = datetime.now()
    changes = {x: {"owner": {"old": "root", "current": "inmanta"}} for x in resource_ids}
    result = await aclient.resource_action_update(environment, resource_ids, action_id, "deploy", finished=now, changes=changes)
    assert result.code == 400

    result = await aclient.resource_action_update(
        environment, resource_ids, action_id, "deploy", status=const.ResourceState.deployed, finished=now, changes=changes
    )
    assert result.code == 200

    result = await client.get_version(environment, version)
    assert result.code == 200
    assert result.result["model"]["done"] == 10
    await agent.stop()


@pytest.mark.asyncio
async def test_clear_environment(client, server, clienthelper, environment):
    """
        Test clearing out an environment
    """
    version = await clienthelper.get_version()
    result = await client.put_version(
        tid=environment, version=version, resources=[], unknowns=[], version_info={}, compiler_version=get_compiler_version()
    )
    assert result.code == 200

    result = await client.get_environment(id=environment, versions=10)
    assert result.code == 200
    assert len(result.result["environment"]["versions"]) == 1

    # trigger a compile
    result = await client.notify_change_get(id=environment)
    assert result.code == 200

    # Wait for env directory to appear
    slice = server.get_slice(SLICE_SERVER)
    env_dir = os.path.join(slice._server_storage["environments"], environment)

    while not os.path.exists(env_dir):
        await asyncio.sleep(0.1)

    result = await client.clear_environment(id=environment)
    assert result.code == 200

    assert not os.path.exists(env_dir)

    result = await client.get_environment(id=environment, versions=10)
    assert result.code == 200
    assert len(result.result["environment"]["versions"]) == 0


@pytest.mark.asyncio
async def test_tokens(server_multi, client_multi, environment_multi):
    # Test using API tokens
    test_token = client_multi._transport_instance.token
    token = await client_multi.create_token(environment_multi, ["api"], idempotent=True)
    jot = token.result["token"]

    assert jot != test_token

    client_multi._transport_instance.token = jot

    # try to access a non environment call (global)
    result = await client_multi.list_environments()
    assert result.code == 401

    result = await client_multi.list_versions(environment_multi)
    assert result.code == 200

    token = await client_multi.create_token(environment_multi, ["agent"], idempotent=True)
    agent_jot = token.result["token"]

    client_multi._transport_instance.token = agent_jot
    result = await client_multi.list_versions(environment_multi)
    assert result.code == 401


def make_source(collector, filename, module, source, req):
    myhash = hash_file(source.encode())
    collector[myhash] = [filename, module, source, req]
    return collector


@pytest.mark.asyncio(timeout=30)
async def test_code_upload(server_multi, client_multi, agent_multi, environment_multi):
    """ Test upload of a single code definition
    """
    version = (await client_multi.reserve_version(environment_multi)).result["data"]

    resources = [
        {
            "group": "root",
            "hash": "89bf880a0dc5ffc1156c8d958b4960971370ee6a",
            "id": "std::File[vm1.dev.inmanta.com,path=/etc/sysconfig/network],v=%d" % version,
            "owner": "root",
            "path": "/etc/sysconfig/network",
            "permissions": 644,
            "purged": False,
            "reload": False,
            "requires": [],
            "version": version,
        }
    ]

    res = await client_multi.put_version(
        tid=environment_multi,
        version=version,
        resources=resources,
        unknowns=[],
        version_info={},
        compiler_version=get_compiler_version(),
    )
    assert res.code == 200

    sources = make_source({}, "a.py", "std.test", "wlkvsdbhewvsbk vbLKBVWE wevbhbwhBH", [])
    sources = make_source(sources, "b.py", "std.xxx", "rvvWBVWHUvejIVJE UWEBVKW", ["pytest"])

    res = await client_multi.upload_code(tid=environment_multi, id=version, resource="std::File", sources=sources)
    assert res.code == 200

    res = await agent_multi._client.get_code(tid=environment_multi, id=version, resource="std::File")
    assert res.code == 200
    assert res.result["sources"] == sources


@pytest.mark.asyncio(timeout=30)
async def test_batched_code_upload(
    server_multi, client_multi, sync_client_multi, environment_multi, agent_multi, snippetcompiler
):
    """ Test uploading all code definitions at once
    """
    config.Config.set("compiler_rest_transport", "request_timeout", "1")

    snippetcompiler.setup_for_snippet(
        """
    h = std::Host(name="test", os=std::linux)
    f = std::ConfigFile(host=h, path="/etc/motd", content="test", purge_on_delete=true)
    """
    )
    version, _ = await snippetcompiler.do_export_and_deploy(do_raise=False)

    code_manager = loader.CodeManager()

    for type_name, resource_definition in resources.resource.get_resources():
        code_manager.register_code(type_name, resource_definition)

    for type_name, handler_definition in handler.Commander.get_providers():
        code_manager.register_code(type_name, handler_definition)

    await asyncio.get_event_loop().run_in_executor(
        None, lambda: upload_code(sync_client_multi, environment_multi, version, code_manager)
    )

    for name, source_info in code_manager.get_types():
        res = await agent_multi._client.get_code(tid=environment_multi, id=version, resource=name)
        assert res.code == 200
        assert len(source_info) == 1
        info = source_info[0]
        assert info.hash in res.result["sources"]
        code = res.result["sources"][info.hash]

        assert info.content == code[2]
        assert info.requires == code[3]


@pytest.mark.asyncio(timeout=30)
async def test_resource_action_log(server_multi, client_multi, environment_multi):
    version = (await client_multi.reserve_version(environment_multi)).result["data"]
    resources = [
        {
            "group": "root",
            "hash": "89bf880a0dc5ffc1156c8d958b4960971370ee6a",
            "id": "std::File[vm1.dev.inmanta.com,path=/etc/sysconfig/network],v=%d" % version,
            "owner": "root",
            "path": "/etc/sysconfig/network",
            "permissions": 644,
            "purged": False,
            "reload": False,
            "requires": [],
            "version": version,
        }
    ]
    res = await client_multi.put_version(
        tid=environment_multi,
        version=version,
        resources=resources,
        unknowns=[],
        version_info={},
        compiler_version=get_compiler_version(),
    )
    assert res.code == 200

    resource_action_log = server_multi.get_slice(SLICE_RESOURCE).get_resource_action_log_file(environment_multi)
    assert os.path.isfile(resource_action_log)
    assert os.stat(resource_action_log).st_size != 0


@pytest.mark.asyncio(timeout=30)
async def test_invalid_sid(server_multi, client_multi, environment_multi):
    """
        Test the server to manage the updates on a model during agent deploy
    """
    # request get_code with a compiler client that does not have a sid
    res = await client_multi.get_code(tid=environment_multi, id=1, resource="std::File")
    assert res.code == 400
    assert res.result["message"] == "Invalid request: this is an agent to server call, it should contain an agent session id"


@pytest.mark.asyncio(timeout=30)
async def test_get_param(server, client, environment):
    metadata = {"key1": "val1", "key2": "val2"}
    await client.set_param(environment, "param", "source", "val", "", metadata, False)
    await client.set_param(environment, "param2", "source2", "val2", "", {"a": "b"}, False)

    res = await client.list_params(tid=environment, query={"key1": "val1"})
    assert res.code == 200
    parameters = res.result["parameters"]
    assert len(parameters) == 1
    metadata_received = parameters[0]["metadata"]
    assert len(metadata_received) == 2
    for k, v in metadata.items():
        assert k in metadata_received
        assert metadata_received[k] == v

    res = await client.list_params(tid=environment, query={})
    assert res.code == 200
    parameters = res.result["parameters"]
    assert len(parameters) == 2


@pytest.mark.asyncio(timeout=30)
async def test_server_logs_address(server_config, caplog):
    with caplog.at_level(logging.INFO):
        ibl = InmantaBootloader()
        await ibl.start()

        client = Client("client")
        result = await client.create_project("env-test")
        assert result.code == 200
        address = "127.0.0.1"

        await ibl.stop()
        log_contains(caplog, "protocol.rest", logging.INFO, f"Server listening on {address}:")
