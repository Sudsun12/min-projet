import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, font

# Simple To-Do List Application in Python

class TodoList:
    def __init__(self):
        self.tasks = {}
        self.file_path = "tasks.json"
        self.load_tasks()
        self.next_id = self._get_next_id()
    
    def _get_next_id(self):
        """Obtenir le prochain ID disponible"""
        return max([0] + list(map(int, self.tasks.keys()))) + 1
    
    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.tasks = json.load(file)
    
    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, description, priority, due_date):
        """Add a new task"""
        # Validate priority
        if priority not in ['one', 'two', 'three']:
            raise ValueError("Invalid priority")
        
        # Validate and standardize date format
        try:
            # Convertir la date en format standard
            parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")

        task_id = self.next_id
        self.tasks[str(task_id)] = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": formatted_date,
            "completed": False
        }
        self.next_id += 1
        self.save_tasks()
        return task_id

    def view_tasks(self):
        """View all tasks"""
        return self.tasks

    def update_task(self, task_id, updated_task):
        """Update a task"""
        if task_id in self.tasks:
            self.tasks[task_id].update(updated_task)
            self.save_tasks()
        else:
            raise ValueError("Task not found")

    def delete_task(self, task_id):
        """Delete a task"""
        str_task_id = str(task_id)
        if str_task_id in self.tasks:
            del self.tasks[str_task_id]
            self.save_tasks()
        else:
            raise ValueError("Task not found")

    def complete_task(self, task_id):
        """Mark a task as complete"""
        str_task_id = str(task_id)
        if str_task_id in self.tasks:
            self.tasks[str_task_id]["completed"] = True
            self.save_tasks()
        else:
            raise ValueError("Task not found")

    def search_task_by_title(self, search_title):
        """Search tasks by title"""
        return {task_id: task_info 
                for task_id, task_info in self.tasks.items() 
                if search_title.lower() in task_info['title'].lower()}

class TodoListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Liste de Tâches")
        self.todo = TodoList()
        
        # Configuration du style
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", foreground="#333333")
        style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Priority.TButton", padding=5, background="#4CAF50")
        
        # Frame principal avec couleur de fond
        self.main_frame = ttk.Frame(self.root, padding="10", style="Custom.TFrame")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.configure(bg="#e6e6e6")
        
        # Créer un frame pour contenir le Treeview et les scrollbars
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=5, sticky='nsew')

        # Configurer les scrollbars
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal")
        
        # Configurer le Treeview avec les scrollbars
        self.task_tree = ttk.Treeview(self.tree_frame, 
                                     columns=('ID', 'Titre', 'Description', 'Priorité', 'Date', 'Statut'),
                                     style="Custom.Treeview",
                                     show='headings',
                                     yscrollcommand=self.vsb.set,
                                     xscrollcommand=self.hsb.set)

        # Configurer les scrollbars pour contrôler le Treeview
        self.vsb.configure(command=self.task_tree.yview)
        self.hsb.configure(command=self.task_tree.xview)

        # Positionner les éléments avec grid
        self.task_tree.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')

        # Configurer l'expansion du grid
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        # Configuration des colonnes (comme avant)
        self.task_tree.heading('ID', text='#️⃣ ID')
        self.task_tree.heading('Titre', text='📌 Titre')
        self.task_tree.heading('Description', text='📝 Description')
        self.task_tree.heading('Priorité', text='⭐ Priorité')
        self.task_tree.heading('Date', text='📅 Date')
        self.task_tree.heading('Statut', text='✔️ Statut')
        
        # Configurer la largeur des colonnes
        self.task_tree.column('ID', width=50, minwidth=50)
        self.task_tree.column('Titre', width=150, minwidth=150)
        self.task_tree.column('Description', width=200, minwidth=200)
        self.task_tree.column('Priorité', width=100, minwidth=100)
        self.task_tree.column('Date', width=100, minwidth=100)
        self.task_tree.column('Statut', width=100, minwidth=100)

        # Configurer l'expansion de la fenêtre principale
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Ajout de couleurs pour les priorités
        self.task_tree.tag_configure('priority_one', background='#ffcdd2')  # Rouge clair
        self.task_tree.tag_configure('priority_two', background='#fff9c4')  # Jaune clair
        self.task_tree.tag_configure('priority_three', background='#c8e6c9')  # Vert clair
        self.task_tree.tag_configure('completed', background='#e0e0e0')  # Gris pour les tâches terminées
        
        # Ajouter un frame pour la recherche (après le tree_frame)
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky='ew')

        # Barre de recherche
        ttk.Label(self.search_frame, text="🔍 Rechercher:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_var.trace('w', self.search_tasks)

        # Frame pour les boutons (déplacer les boutons existants ici)
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=5)

        # Boutons
        ttk.Button(self.button_frame, 
                  text="➕ Ajouter Tâche", 
                  command=self.add_task_window,
                  style="Priority.TButton").pack(side='left', padx=5)
        
        ttk.Button(self.button_frame, 
                  text="✏️ Modifier Tâche", 
                  command=self.update_task_window,
                  style="Priority.TButton").pack(side='left', padx=5)
        
        ttk.Button(self.button_frame, 
                  text="❌ Supprimer Tâche", 
                  command=self.delete_task,
                  style="Priority.TButton").pack(side='left', padx=5)
        
        ttk.Button(self.button_frame, 
                  text="✔️ Marquer Terminé", 
                  command=self.complete_task,
                  style="Priority.TButton").pack(side='left', padx=5)

        # Initialiser le compteur de tâches
        self.task_counter = ttk.Label(self.main_frame, text="")
        self.task_counter.grid(row=3, column=0, columnspan=3, pady=10)

        self.refresh_task_list()

    def refresh_task_list(self):
        # Nettoyer la liste existante
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Compteurs pour les statistiques
        total_tasks = 0
        completed_tasks = 0
        ongoing_tasks = 0
        
        tasks = self.todo.view_tasks()
        for task_id, task in tasks.items():
            status = "✅ Terminé" if task['completed'] else "🔄 En cours"
            tags = ()
            
            # Mettre à jour les compteurs
            total_tasks += 1
            if task['completed']:
                completed_tasks += 1
                tags = ('completed',)
            else:
                ongoing_tasks += 1
                if task['priority'] == 'one':
                    tags = ('priority_one',)
                elif task['priority'] == 'two':
                    tags = ('priority_two',)
                elif task['priority'] == 'three':
                    tags = ('priority_three',)
            
            self.task_tree.insert('', 'end', values=(
                task_id,
                task['title'],
                task['description'],
                self.get_priority_emoji(task['priority']),
                task['due_date'],
                status
            ), tags=tags)
        
        # Mettre à jour le compteur
        self.task_counter.configure(
            text=f"📊 Tâches totales: {total_tasks} | ✅ Terminées: {completed_tasks} | 🔄 En cours: {ongoing_tasks}"
        )

    def get_priority_emoji(self, priority):
        priority_emojis = {
            'one': '🔴 Haute',
            'two': '🟡 Moyenne',
            'three': '🟢 Basse'
        }
        return priority_emojis.get(priority, priority)

    def add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ Ajouter une Tâche")
        add_window.configure(bg="#e6e6e6")
        
        # Rendre la fenêtre modale (bloquer l'interaction avec la fenêtre principale)
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Style pour la fenêtre d'ajout
        style = ttk.Style()
        style.configure("Add.TLabel", padding=5)
        style.configure("Add.TButton", padding=5)
        
        ttk.Label(add_window, text="📌 Titre:", style="Add.TLabel").grid(row=0, column=0, pady=5)
        title_entry = ttk.Entry(add_window, width=30)
        title_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="📝 Description:", style="Add.TLabel").grid(row=1, column=0, pady=5)
        desc_entry = ttk.Entry(add_window, width=30)
        desc_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="⭐ Priorité:", style="Add.TLabel").grid(row=2, column=0, pady=5)
        priority_combo = ttk.Combobox(add_window, 
                                    values=['one - 🔴 Haute', 'two - 🟡 Moyenne', 'three - 🟢 Basse'],
                                    width=27)
        priority_combo.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(add_window, text="📅 Date (YYYY-MM-DD):", style="Add.TLabel").grid(row=3, column=0, pady=5)
        date_entry = ttk.Entry(add_window, width=30)
        date_entry.grid(row=3, column=1, pady=5, padx=5)

        def save_task():
            try:
                priority = priority_combo.get().split(' - ')[0]
                self.todo.add_task(
                    title_entry.get(),
                    desc_entry.get(),
                    priority,
                    date_entry.get()
                )
                add_window.destroy()
                self.refresh_task_list()  # Déplacé après la destruction de la fenêtre
                messagebox.showinfo("✅ Succès", "Tâche ajoutée avec succès!")
            except ValueError as e:
                messagebox.showerror("❌ Erreur", str(e))
        
        # Gérer la fermeture de la fenêtre avec le bouton X
        def on_closing():
            add_window.grab_release()
            add_window.destroy()
        
        add_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        ttk.Button(add_window, 
                  text="💾 Sauvegarder", 
                  command=save_task,
                  style="Add.TButton").grid(row=4, column=0, columnspan=2, pady=10)

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner une tâche à supprimer")
            return
        
        try:
            task_id = self.task_tree.item(selected_item)['values'][0]
            self.todo.delete_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("✅ Succès", "Tâche supprimée avec succès!")
        except ValueError as e:
            messagebox.showerror("❌ Erreur", str(e))

    def complete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner une tâche à terminer")
            return
        
        try:
            task_id = self.task_tree.item(selected_item)['values'][0]
            self.todo.complete_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("✅ Succès", "Tâche marquée comme terminée!")
        except ValueError as e:
            messagebox.showerror("❌ Erreur", str(e))

    def search_tasks(self, *args):
        search_term = self.search_var.get().lower()
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        tasks = self.todo.view_tasks()
        for task_id, task in tasks.items():
            if (search_term in task['title'].lower() or 
                search_term in task['description'].lower()):
                status = "✅ Terminé" if task['completed'] else "🔄 En cours"
                tags = self.get_task_tags(task)
                
                self.task_tree.insert('', 'end', values=(
                    task_id,
                    task['title'],
                    task['description'],
                    self.get_priority_emoji(task['priority']),
                    task['due_date'],
                    status
                ), tags=tags)

    def update_task_window(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("⚠️ Attention", "Veuillez sélectionner une tâche à modifier")
            return

        task_id = self.task_tree.item(selected_item)['values'][0]
        task = self.todo.tasks[str(task_id)]

        update_window = tk.Toplevel(self.root)
        update_window.title("✏️ Modifier la Tâche")
        update_window.configure(bg="#e6e6e6")
        update_window.transient(self.root)
        update_window.grab_set()

        ttk.Label(update_window, text="📌 Titre:").grid(row=0, column=0, pady=5)
        title_entry = ttk.Entry(update_window, width=30)
        title_entry.insert(0, task['title'])
        title_entry.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(update_window, text="📝 Description:").grid(row=1, column=0, pady=5)
        desc_entry = ttk.Entry(update_window, width=30)
        desc_entry.insert(0, task['description'])
        desc_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(update_window, text="⭐ Priorité:").grid(row=2, column=0, pady=5)
        priority_combo = ttk.Combobox(update_window, 
                                    values=['one - 🔴 Haute', 'two - 🟡 Moyenne', 'three - 🟢 Basse'],
                                    width=27)
        priority_combo.set(f"{task['priority']} - {self.get_priority_emoji(task['priority'])}")
        priority_combo.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(update_window, text="📅 Date (YYYY-MM-DD):").grid(row=3, column=0, pady=5)
        date_entry = ttk.Entry(update_window, width=30)
        date_entry.insert(0, task['due_date'])
        date_entry.grid(row=3, column=1, pady=5, padx=5)

        def save_updates():
            try:
                priority = priority_combo.get().split(' - ')[0]
                updated_task = {
                    "title": title_entry.get(),
                    "description": desc_entry.get(),
                    "priority": priority,
                    "due_date": date_entry.get(),
                    "completed": task['completed']
                }
                self.todo.update_task(str(task_id), updated_task)
                update_window.destroy()
                self.refresh_task_list()
                messagebox.showinfo("✅ Succès", "Tâche mise à jour avec succès!")
            except ValueError as e:
                messagebox.showerror("❌ Erreur", str(e))

        ttk.Button(update_window, 
                  text="💾 Sauvegarder", 
                  command=save_updates,
                  style="Add.TButton").grid(row=4, column=0, columnspan=2, pady=10)

    def get_task_tags(self, task):
        if task['completed']:
            return ('completed',)
        elif task['priority'] == 'one':
            return ('priority_one',)
        elif task['priority'] == 'two':
            return ('priority_two',)
        elif task['priority'] == 'three':
            return ('priority_three',)
        return ()

def main():
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()