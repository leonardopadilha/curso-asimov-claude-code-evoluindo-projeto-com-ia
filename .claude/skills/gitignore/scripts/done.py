import sys

def is_task_done(skill_gitignore, project_gitignore) -> bool:
    """Verifica se o .gitignore fornecido pela SKILL está contido no .gitignore do projeto."""

    try:
        with open(skill_gitignore, 'r', encoding='utf-8') as skill_file, \
             open(project_gitignore, 'r', encoding='utf-8') as proj_file:

             set_skill = set(line.strip() for line in skill_file if line)
             set_project = set(line.strip() for line in proj_file if line)

             return set_skill.issubset(set_project) # retorna True se o set_skill está contido no set_project, False caso contrário

    except FileNotFoundError:
        return False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        skill_gitignore = sys.argv[1]
        project_gitignore = sys.argv[2]

        result = is_task_done(skill_gitignore, project_gitignore)

        print(f"Conteúdo do arquivo {skill_gitignore} está incluso no arquivo {project_gitignore}: ", result)
    else:
        print("Número de argumentos do script está errado!")