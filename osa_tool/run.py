import os
from typing import List

from osa_tool.analytics.report_maker import ReportGenerator
from osa_tool.analytics.sourcerank import SourceRank
from osa_tool.arguments_parser import get_cli_args
from osa_tool.config.settings import ConfigLoader, GitSettings
from osa_tool.convertion.notebook_converter import NotebookConverter
from osa_tool.github_agent.github_agent import GithubAgent
from osa_tool.osatreesitter.docgen import DocGen
from osa_tool.osatreesitter.osa_treesitter import OSA_TreeSitter
<<<<<<< HEAD
from osa_tool.readmeai.config.settings import ConfigLoader, GitSettings
from osa_tool.readmeai.readmegen_article.config.settings import ArticleConfigLoader
from osa_tool.readmeai.readme_core import readme_agent
from osa_tool.readmeai.utils.file_handler import FileHandler
from osa_tool.translation.dir_translator import DirectoryTranslator
from osa_tool.convertion.notebook_converter import NotebookConverter
from osa_tool.utils import delete_repository, osa_project_root, parse_folder_name
=======
from osa_tool.readmegen.readme_core import readme_agent
from osa_tool.translation.dir_translator import DirectoryTranslator
from osa_tool.utils import (
    delete_repository,
    logger,
    parse_folder_name
)
>>>>>>> ebc0349e0f0dc1e78405c57378098610cc4c277d


def main():
    """Main function to generate a README.md file for a GitHub repository.

    Handles command-line arguments, clones the repository, creates and checks out a branch,
    generates the README.md file, and commits and pushes the changes.
    """

    # Create a command line argument parser
    args = get_cli_args()
    repo_url = args.repository
    api = args.api
    base_url = args.base_url
    model_name = args.model
    article = args.article
    notebook_paths = args.convert_notebooks

    try:
        # Load configurations and update
        config = load_configuration(repo_url, api, base_url, model_name)

        # Initialize GitHub agent and perform operations
        github_agent = GithubAgent(repo_url)
        github_agent.star_repository()
        github_agent.create_fork()
        github_agent.clone_repository()
        github_agent.create_and_checkout_branch()

        # .ipynb to .py convertion
        if notebook_paths is not None:
            convert_notebooks(config, notebook_paths)

        # Repository Analysis Report generation
        sourcerank = SourceRank(config)
        analytics = ReportGenerator(config, sourcerank)
        analytics.build_pdf()

        # Auto translating names of directories
        if args.translate_dirs:
            translation = DirectoryTranslator(config)
            translation.rename_directories_and_files()

        # Docstring generation
        generate_docstrings(config)

        # License compiling
        if not sourcerank.license_presence():
            compile_license_file(sourcerank)

        # Readme generation
        readme_agent(config, article)

        github_agent.commit_and_push_changes()
        github_agent.create_pull_request()

        if args.delete_dir:
            delete_repository(repo_url)

        logger.info("All operations completed successfully.")
    except Exception as e:
        logger.error("Error: %s", e, exc_info=True)


def convert_notebooks(
    config_loader: ConfigLoader, notebook_paths: List[str] | None = None
) -> None:
    """Converts Jupyter notebooks to Python scripts based on provided paths.

    Args:
        config_loader: The configuration object which contains repo_url.
        notebook_paths: A list of paths to the notebooks to be converted (or None).
                        If empty, the converter will process the current repository.
    """
    try:
        converter = NotebookConverter()
        if len(notebook_paths) == 0:
            repo_url = config_loader.config.git.repository
            converter.process_path(os.path.basename(repo_url))
        else:
            for path in notebook_paths:
                converter.process_path(path)

    except Exception as e:
        logger.error("Error while converting notebooks: %s", repr(e), exc_info=True)


def compile_license_file(sourcerank: SourceRank):
    """
    Compiles a license file for a software project using a specified template.

    This method takes a SourceRank object as input, extracts necessary information such as creation year and author
    to compile a license file based on a predefined template. The compiled license file is then saved in the repository
    directory of the SourceRank object.

    Parameters:
        - sourcerank: SourceRank object containing metadata about the software project.

    Returns:
        None. The compiled license file is saved in the repository directory of the SourceRank object.
    """
    try:
        logger.info("LICENSE was not resolved, compiling started...")
        license_template_path = os.path.join(
            os.getcwd(), "osa_tool", "docs", "license_template", "licenses.toml"
        )
        license_template = FileHandler().read_toml(license_template_path)
        license_type = "bsd"
        year = sourcerank.metadata.created_at[:4]
        author = sourcerank.metadata.owner
        license_text = license_template[license_type]["template"].format(
            year=year, author=author
        )
        license_output_path = os.path.join(sourcerank.repo_path, "LICENSE")
        with open(license_output_path, "w") as f:
            f.write(license_text)
        logger.info(
            f"""LICENSE has been successfully compiled at {os.path.join(sourcerank.repo_path, "LICENSE")}"""
        )
    except Exception as e:
        logger.error("Error while compiling LICENSE: %s", e, exc_info=True)


def generate_docstrings(config_loader: ConfigLoader) -> None:
    """Generates a docstrings for .py's classes and methods of the provided repository.

    Args:
        config_loader: The configuration object which contains settings for osa_tool.

    """
    try:
        repo_url = config_loader.config.git.repository
        ts = OSA_TreeSitter(parse_folder_name(repo_url))
        res = ts.analyze_directory(ts.cwd)
        dg = DocGen(config_loader)
        dg.process_python_file(res)

    except Exception as e:
        logger.error("Error while docstring generation: %s", repr(e), exc_info=True)


def load_configuration(
<<<<<<< HEAD
    repo_url: str, api: str, base_url: str, model_name: str, article: str | None
=======
        repo_url: str,
        api: str,
        base_url: str,
        model_name: str,
>>>>>>> ebc0349e0f0dc1e78405c57378098610cc4c277d
) -> ConfigLoader:
    """
    Loads configuration for osa_tool.

    Args:
        repo_url: URL of the GitHub repository.
        api: LLM API service provider.
        base_url: URL of the provider compatible with API OpenAI
        model_name: Specific LLM model to use.

    Returns:
        config_loader: The configuration object which contains settings for osa_tool.
    """
<<<<<<< HEAD
    if article is None:

        config_loader = ConfigLoader(
            config_dir=os.path.join(osa_project_root(), "config", "standart")
        )
    else:
        config_loader = ArticleConfigLoader(
            config_dir=os.path.join(osa_project_root(), "config", "with_article")
        )
=======
    config_loader = ConfigLoader()
>>>>>>> ebc0349e0f0dc1e78405c57378098610cc4c277d

    config_loader.config.git = GitSettings(repository=repo_url)
    config_loader.config.llm = config_loader.config.llm.model_copy(
        update={"api": api, "url": base_url, "model": model_name}
    )
    logger.info("Config successfully updated and loaded")
    return config_loader


if __name__ == "__main__":
    main()
