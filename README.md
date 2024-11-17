### Prerequisite

- MySQL Database
- Configure MySQL credentials on config.py

### Setup MySQL Schemas

```
CREATE TABLE `Users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
);
```

```

CREATE TABLE `Books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `genre` varchar(255) DEFAULT NULL,
  `item_condition` enum('New','Good','Used') NOT NULL,
  `availability` enum('Lend','Exchange','NotAvailable') NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`book_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
);
```

### Run instructions for sending data to SigNoz

- Create a virtual environment and activate it

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies

```
pip install -r requirements.txt
```

- Run the application
```
python app.py
```
- Access the Application
The default flask application will listen on localhost:5000