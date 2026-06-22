from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AgentExecutionResult:
    executor_name: str
    command_template: str
    returncode: int
    prompt_path: Path
    stdout_path: Path
    stderr_path: Path
    metadata_path: Path

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "executor_name": self.executor_name,
            "command_template": self.command_template,
            "returncode": self.returncode,
            "succeeded": self.succeeded,
            "prompt_path": str(self.prompt_path),
            "stdout_path": str(self.stdout_path),
            "stderr_path": str(self.stderr_path),
            "metadata_path": str(self.metadata_path),
        }


class ClaudeCodeExecutor:
    """Run a generated research prompt through a local Claude Code CLI.

    This executor intentionally keeps the Claude command configurable because
    Claude Code installations and preferred permission modes may differ.

    Default behavior:

        command_template = "claude --print"

    The prompt is sent to the process through stdin.

    If your local CLI expects a file path instead, use a command template with
    the placeholder {prompt_file}, for example:

        claude --print {prompt_file}

    The placeholder is replaced with the generated prompt file path.

    Avoid using shell interpolation of raw prompt text. Passing the prompt by
    stdin or by file is safer and more reliable for long mathematical prompts.
    """

    def __init__(
        self,
        *,
        project_root: Path,
        command_template: str | None = None,
        timeout_seconds: int = 3600,
    ) -> None:
        self.project_root = project_root
        self.command_template = (
            command_template
            or os.environ.get("PSA_CLAUDE_COMMAND")
            or "claude --print"
        )
        self.timeout_seconds = timeout_seconds

    def run(
        self,
        *,
        prompt: str,
        prompt_path: Path,
        problem_id: str,
        decision: str,
        round_index: int,
    ) -> AgentExecutionResult:
        log_dir = self.project_root / "logs" / "claude"
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_decision = self._safe_name(decision)
        prefix = f"{timestamp}_{problem_id}_round{round_index}_{safe_decision}"

        archived_prompt_path = log_dir / f"{prefix}_prompt.md"
        stdout_path = log_dir / f"{prefix}_stdout.txt"
        stderr_path = log_dir / f"{prefix}_stderr.txt"
        metadata_path = log_dir / f"{prefix}_metadata.json"

        archived_prompt_path.write_text(prompt, encoding="utf-8")

        command = self._build_command(prompt_path=prompt_path)

        metadata: dict[str, Any] = {
            "executor_name": "ClaudeCodeExecutor",
            "problem_id": problem_id,
            "decision": decision,
            "round_index": round_index,
            "command_template": self.command_template,
            "command_executed": command,
            "prompt_path": str(prompt_path),
            "archived_prompt_path": str(archived_prompt_path),
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "timeout_seconds": self.timeout_seconds,
            "started_at": datetime.now().isoformat(timespec="seconds"),
        }

        try:
            completed = subprocess.run(
                command,
                cwd=self.project_root,
                input=None if "{prompt_file}" in self.command_template else prompt,
                capture_output=True,
                text=True,
                shell=True,
                timeout=self.timeout_seconds,
            )

            stdout_path.write_text(completed.stdout or "", encoding="utf-8")
            stderr_path.write_text(completed.stderr or "", encoding="utf-8")

            metadata.update(
                {
                    "finished_at": datetime.now().isoformat(timespec="seconds"),
                    "returncode": completed.returncode,
                    "timed_out": False,
                }
            )

            metadata_path.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            return AgentExecutionResult(
                executor_name="ClaudeCodeExecutor",
                command_template=self.command_template,
                returncode=completed.returncode,
                prompt_path=archived_prompt_path,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                metadata_path=metadata_path,
            )

        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""

            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", errors="replace")
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", errors="replace")

            stdout_path.write_text(stdout, encoding="utf-8")
            stderr_path.write_text(stderr, encoding="utf-8")

            metadata.update(
                {
                    "finished_at": datetime.now().isoformat(timespec="seconds"),
                    "returncode": -1,
                    "timed_out": True,
                    "error": f"Claude Code command timed out after {self.timeout_seconds} seconds.",
                }
            )

            metadata_path.write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            return AgentExecutionResult(
                executor_name="ClaudeCodeExecutor",
                command_template=self.command_template,
                returncode=-1,
                prompt_path=archived_prompt_path,
                stdout_path=stdout_path,
                stderr_path=stderr_path,
                metadata_path=metadata_path,
            )

    def _build_command(self, *, prompt_path: Path) -> str:
        if "{prompt_file}" not in self.command_template:
            return self.command_template

        quoted_prompt_path = f'"{prompt_path}"'
        return self.command_template.replace("{prompt_file}", quoted_prompt_path)

    def _safe_name(self, value: str) -> str:
        chars: list[str] = []
        for char in value.lower():
            if char.isalnum():
                chars.append(char)
            else:
                chars.append("_")
        collapsed = "".join(chars).strip("_")
        return collapsed or "decision"
