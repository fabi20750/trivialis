from flask import current_app
from flask_security import hash_password

from app import db
from app.models import Language, Profile, Role, Story, Task, Answer

#Function to create languages
def create_languages(): 
  for l in current_app.config['LANGUAGES']:
    db.session.add(Language(name=l['name'], isoCode=l['isoCode'], icon=l['icon']))
  db.session.commit()
  return True

#Function to create roles
def create_roles():
  for r in current_app.config['USER_ROLES']:
    current_app.security.datastore.find_or_create_role(
      name = r['name'],
      description = r['description'],
      permissions = r['permissions']
    )
  db.session.commit()
  return True

#Function to create users
def create_users(adminUsername, adminEmail, adminPassword, adminLanguage):
  for r in Role.query.all():
    if r.name == 'Admin':
      current_app.security.datastore.create_user(
        email = adminEmail,
        username = adminUsername,
        password = hash_password(adminPassword),
        roles = ['Admin']
      )
      # Override admin language with selected language
      db.session.commit()
      adminProfile = Profile.query.first()
      adminProfile.languageId = adminLanguage
    else:
      current_app.security.datastore.create_user(
        email = r.name+'@salerva.ch',
        username = r.name,
        password = hash_password(r.name+'123'),
        roles = [r.name]
      )
  db.session.commit()
  return True

#Function to create stories
def create_stories():
  # Clear existing stories
  Story.query.delete()
  db.session.commit()
  
  stories = [
    
    Story(id=1, languageId=2, name='aware.swiss', description='Dies ist die erste Geschichte.', is_active=True),
    Story(id=2, languageId=2, name='Computerfehler', description='Während du deine Hausaufgaben machst, hört dein Computer plötzlich auf zu funktionieren. Arbeite durch diese Geschichte, um herauszufinden, was passiert ist.', is_active=True),
    Story(id=3, languageId=2, name='News Artikel', description='Du arbeitest als Nachrichtenreporter und musst deine Geschichte morgen früh abliefern. Leider hast du noch nicht mit dem Schreiben begonnen. Finde heraus, wie KI dir helfen kann, den Artikel rechtzeitig zu schreiben.', is_active=True),
    Story(id=4, languageId=2, name='Eigene Website', description='Du möchtest eine Website veröffentlichen. Du hast den Inhalt erstellt und musst jetzt herausfinden, wie du den Inhalt im Internet verfügbar machen kannst.', is_active=True),
    Story(id=5, languageId=2, name='Google Werbung', description='Wird noch geschrieben', is_active=True),
    Story(id=6, languageId=2, name='Anruf von deinen Eltern', description='Wird noch geschrieben', is_active=True),
    Story(id=7, languageId=2, name='Paketlieferung', description='Wird noch geschrieben', is_active=True),
    Story(id=8, languageId=2, name='Kostenlose Dienste', description='Oder was ist das Produkt?', is_active=True),
    Story(id=9, languageId=2, name='Liebe auf den ersten Klick', description='Wird noch geschrieben', is_active=True),
    Story(id=10, languageId=2, name='Aber ich habe die Nachricht gelöscht', description='Wird noch geschrieben', is_active=True),
    Story(id=11, languageId=2, name='Schnelles Geld', description='Willst du schnell reich werden', is_active=True)
   
  ]
  for story in stories:
    db.session.add(story)
  db.session.commit()
  stories = Story.query.all()
  return stories

#Function to create tasks
def create_tasks():
  # Clear existing tasks
  Task.query.delete()
  db.session.commit()
  
  tasks = [
      Task(id=1, storyId=1, name='Welche Gefahren lauern im Internet?', description='Identifizieren Sie die verschiedenen Bedrohungen, die im Internet existieren.', type='multiple_choice', points=10),
      Task(id=2, storyId=1, name='Sei schlauer als ein Hacker', description='Lernen Sie, wie Sie potenzielle Hacker mit diesen Tipps überlisten können.', type='multiple_choice', points=10),
      Task(id=3, storyId=1, name='Lesen Sie über Internetsicherheit', description='Eine Einführung in die Internetsicherheit.', type='read', points=5, read_text='Das Internet ist eine riesige Ressource voller Informationen und Möglichkeiten, bringt jedoch auch Risiken mit sich. Es ist entscheidend, sich der potenziellen Bedrohungen wie Malware, Phishing und Identitätsdiebstahl bewusst zu sein. Verwenden Sie immer starke, einzigartige Passwörter für Ihre Konten, seien Sie vorsichtig beim Klicken auf Links oder beim Herunterladen von Anhängen aus unbekannten Quellen und halten Sie Ihre Software und Antivirenprogramme auf dem neuesten Stand. Denken Sie daran, Ihre Online-Sicherheit liegt in Ihren Händen.'),
      Task(id=4, storyId=1, name='Was ist Phishing?', description='Wählen Sie die richtige Definition von Phishing.', type='multiple_choice', points=10),
      Task(id=5, storyId=1, name='Wie man ein starkes Passwort erstellt', description='Lernen Sie die Grundlagen der Erstellung starker Passwörter.', type='read', points=5, read_text='Ein starkes Passwort ist Ihre erste Verteidigungslinie gegen unbefugten Zugriff auf Ihre Konten. Hier sind einige Richtlinien zur Erstellung starker Passwörter: 1) Verwenden Sie eine Mischung aus Groß- und Kleinbuchstaben, Zahlen und Symbolen. 2) Machen Sie es mindestens 12 Zeichen lang. 3) Vermeiden Sie persönliche Informationen wie Geburtsdaten oder Namen. 4) Verwenden Sie keine gängigen Wörter oder Phrasen. 5) Verwenden Sie für jedes Konto ein einzigartiges Passwort. Ziehen Sie in Betracht, einen Passwort-Manager zu verwenden, um Ihnen zu helfen, komplexe Passwörter sicher zu erstellen und zu speichern.'),
      Task(id=6, storyId=1, name='Was ist Malware?', description='Wählen Sie die richtige Antwort über Malware.', type='multiple_choice', points=10),
      Task(id=7, storyId=1, name='Verstehen von Datenschutzeinstellungen', description='Lernen Sie, wie Sie Datenschutzeinstellungen in sozialen Medien verwalten.', type='read', points=5, read_text='Soziale Medienplattformen bieten verschiedene Datenschutzeinstellungen, um Ihnen zu helfen, zu kontrollieren, wer Ihre Informationen sehen kann. Es ist wichtig, diese Einstellungen regelmäßig zu überprüfen und zu aktualisieren. Einige wichtige Bereiche, auf die Sie sich konzentrieren sollten, sind: 1) Profil Sichtbarkeit: Entscheiden Sie, wer Ihre Profilinformationen sehen kann. 2) Beitrags Sichtbarkeit: Kontrollieren Sie, wer Ihre Beiträge und Fotos sehen kann. 3) Freundschaftsanfragen: Legen Sie fest, wer Ihnen Freundschaftsanfragen senden kann. 4) Such Sichtbarkeit: Bestimmen Sie, ob Ihr Profil in Suchergebnissen angezeigt wird. 5) Datennutzung: Verstehen Sie, wie die Plattform Ihre Daten verwendet und passen Sie die Einstellungen entsprechend an. Denken Sie daran, dass die Standardeinstellungen möglicherweise nicht das Maß an Privatsphäre bieten, das Sie wünschen, also nehmen Sie sich die Zeit, sie nach Ihrem Komfortniveau anzupassen.'),
      Task(id=8, storyId=1, name='Was ist ein VPN?', description='Wählen Sie die richtige Antwort zu VPNs.', type='multiple_choice', points=10),
      Task(id=9, storyId=1, name='Sichere Websites erkennen', description='Lernen Sie, wie Sie sichere Websites identifizieren.', type='read', points=5, read_text='Die Identifizierung sicherer Websites ist entscheidend für sicheres Surfen und Online-Transaktionen. Hier sind einige wichtige Indikatoren für eine sichere Website: 1) Achten Sie auf "https" am Anfang der URL. Das "s" steht für sicher. 2) Überprüfen Sie das Vorhandensein eines Vorhängeschloss-Symbols in der Adressleiste. 3) Überprüfen Sie das Sicherheitszertifikat der Website, indem Sie auf das Vorhängeschloss-Symbol klicken. 4) Seien Sie vorsichtig bei Websites mit Rechtschreibfehlern oder unprofessionellem Design. 5) Verwenden Sie aktuelle Browser, die potenziell unsichere Seiten erkennen und warnen können. 6) Seien Sie besonders vorsichtig, wenn Sie sensible Informationen wie Kreditkartendaten oder Passwörter eingeben. Denken Sie daran, dass eine sichere Verbindung nicht die Legitimität einer Website garantiert, also seien Sie immer vorsichtig und verwenden Sie gesunden Menschenverstand.'),
      Task(id=10, storyId=1, name='Was ist Identitätsdiebstahl?', description='Wählen Sie die richtige Definition von Identitätsdiebstahl.', type='multiple_choice', points=10),
  ]
  
  for task in tasks:
    db.session.add(task)
  
  # Populate answers for multiple choice questions
  answers = [
    Answer(task_id=1, text='Phishing', is_correct=False),
    Answer(task_id=1, text='Malware', is_correct=False),
    Answer(task_id=1, text='Identitätsdiebstahl', is_correct=False), 
    Answer(task_id=1, text='Alle oben genannten', is_correct=True),  

    Answer(task_id=2, text='Verwenden Sie eine Mischung aus Buchstaben, Zahlen und Symbolen', is_correct=True),  
    Answer(task_id=2, text='Verwenden Sie Ihr Geburtsdatum', is_correct=False),  
    Answer(task_id=2, text='Verwenden Sie dasselbe Passwort für alles', is_correct=False),  
    Answer(task_id=2, text='Schreiben Sie es auf und bewahren Sie es unter Ihrer Tastatur auf', is_correct=False),  

    Answer(task_id=4, text='Eine Methode, um persönliche Informationen zu stehlen', is_correct=True),  
    Answer(task_id=4, text='Eine Art von Software', is_correct=False),  
    Answer(task_id=4, text='Eine sichere Möglichkeit zu surfen', is_correct=False),  
    Answer(task_id=4, text='Keine der oben genannten', is_correct=False),  

    Answer(task_id=6, text='Software, die Ihren Computer schädigt', is_correct=True),  
    Answer(task_id=6, text='Eine Art von Internetverbindung', is_correct=False),  
    Answer(task_id=6, text='Eine Sicherheitsfunktion', is_correct=False),  
    Answer(task_id=6, text='Keine der oben genannten', is_correct=False),  

    Answer(task_id=8, text='Ein privates Netzwerk', is_correct=True),  
    Answer(task_id=8, text='Eine Art von Virus', is_correct=False),  
    Answer(task_id=8, text='Ein Webbrowser', is_correct=False),  
    Answer(task_id=8, text='Keine der oben genannten', is_correct=False),  

    Answer(task_id=10, text='Die Identität von jemandem stehlen', is_correct=True),  
    Answer(task_id=10, text='Eine Art von Malware', is_correct=False),  
    Answer(task_id=10, text='Ein Phishing-Versuch', is_correct=False),  
    Answer(task_id=10, text='Keine der oben genannten', is_correct=False),  
  ]
  
  for answer in answers:
    db.session.add(answer)
  
  db.session.commit()
  tasks = Task.query.all()
  return tasks

