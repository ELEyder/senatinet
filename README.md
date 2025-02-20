# 📚 Proyecto SENATINET

Este proyecto utiliza **Django**, **SQLite** y **Firestore** para el backend. A continuación se detallan los pasos para configurar el entorno, crear la base de datos y ejecutar el servidor.

---

## 🚀 **Configuración del entorno de desarrollo**

### 1️⃣ **Clonar el repositorio**
```bash
git clone https://github.com/ELEyder/senatinet.git
cd senatinet
```

### 2️⃣ **Crear y activar el entorno virtual**

#### 💻 **Windows**
```bash
python -m venv venv
./venv/Scripts/activate
```

#### 🍏 **macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ **Crear el archivo `.env`**

- Crea un archivo `.env` en la raíz del proyecto siguiendo el ejemplo provisto en `.env.example`.
- Este archivo almacenará variables sensibles como claves secretas o credenciales.

---

### 4️⃣ **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

---

### 5️⃣ **Crear la base de datos SQLite** 🗄️

> Django generará automáticamente `db.sqlite3` al aplicar las migraciones iniciales.

```bash
python manage.py migrate
```

🔧 *Este comando aplica las migraciones necesarias para el funcionamiento básico del proyecto (usuarios, sesiones, admin, etc.).*

---

### 6️⃣ **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

🌐 Accede al servidor en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🛠 **Comandos útiles**

- 📦 **Actualizar `requirements.txt`**:
  ```bash
  pip freeze > requirements.txt
  ```

- 🔄 **Obtener los últimos cambios del repositorio**:
  ```bash
  git fetch origin
  git reset --hard origin/main
  ```

---