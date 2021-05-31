DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS generated_text_plus_feedback;
DROP TABLE IF EXISTS twitter_classification_plus_feedback;

CREATE TABLE  IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  pw_hash TEXT NOT NULL,
);
CREATE TABLE IF NOT EXISTS todoList (


)

CREATE TABLE  IF NOT EXISTS task (

    list_id = db.Column(db.Integer,db.ForeignKey('todoList.id') )

    type = db.Column(db.String(80),nullable=False)
    text = db.Column( db.String(180),nullable=False)
    status = db.Column( db.String(10),nullable=False)
    begin_date =  db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    end_time =  db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rand = db.Column(db.Integer, unique = True)
  list_id = db.Column(db.Integer,db.ForeignKey('todoList.id') )

  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE  IF NOT EXISTS twitter_classification_plus_feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  data TEXT NOT NULL,
  classification INTEGER,
  user_feedback INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id)

);

CREATE TABLE  IF NOT EXISTS generated_text_plus_feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  param_method  INTEGER,
  param_length  INTEGER,
  param_output_size  INTEGER,
  seed TEXT,
  data TEXT,
  score INTEGER,


  FOREIGN KEY (author_id) REFERENCES user (id)

);


CREATE TABLE  IF NOT EXISTS post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);