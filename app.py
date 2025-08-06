from flask import Flask, request, jsonify
from models.task import Task

# __name__ = __main__
app = Flask(__name__)

tasks = []
#criado o id da tarefa
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def create_task():
    #permitindo que acesse a variavel fora do escopo que precise fazer uma interação (task_id_control += 1)
    global task_id_control
    #Receber os dados do cliente
    data = request.get_json()
    #Criar a tarefa
    new_task = Task(id=task_id_control,title=data["title"], description=data.get("description", ""))
    #incrementando o id para cada tarefa ter um unico id
    task_id_control += 1
    #Adicionando na lista
    tasks.append(new_task)
    print(tasks)
    #retorna em Json na api do postman(Padrão REST)
    return jsonify({"message": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Retornando as tarefas criadas
    task_list = [task.to_dict() for task in tasks]

    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
                }
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Não foi possivel encontrar nenhuma tarefa com esse ID"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    #verificando se existe a tarefaa como o id fornecido no parametro
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
        
    if task == None:
        return jsonify({"message": "Não foi possivel encontrar nenhuma tarefa com esse ID"}), 404
    #recuperando o que o usuario digitar

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]
    return jsonify({"message": "Tarefa atualizada com sucesso"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Não foi possivel encontrar nenhuma tarefa com esse ID"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso!"})

#iniciando o app
if __name__ == "__main__":
    app.run(debug=True)
