"""Git command utilities."""

import asyncio


class GitResult:
    """Git command result."""

    def __init__(self, stdout: str, stderr: str, returncode: int):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def text(self) -> str:
        """Get stdout as text."""
        return self.stdout


async def git(args: list[str], cwd: str | None = None) -> GitResult:
    """Execute git command."""
    cmd = ["git"] + args

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
    )

    stdout, stderr = await process.communicate()

    return GitResult(
        stdout=stdout.decode("utf-8"),
        stderr=stderr.decode("utf-8"),
        returncode=process.returncode or 0,
    )
