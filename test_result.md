  - task: "Newsletter-Registrierung: POST /api/newsletter/subscribe"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested newsletter subscription endpoint. The endpoint accepts email and name, returns a success message, and properly stores the subscriber in the database with an unsubscribe token."

  - task: "Newsletter-Abmeldung: POST /api/newsletter/unsubscribe/{token}"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested newsletter unsubscription endpoint. The endpoint accepts a valid unsubscribe token and properly marks the subscriber as inactive in the database."

  - task: "Admin Newsletter-Verwaltung: GET /api/admin/newsletter/subscribers"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested admin newsletter subscribers endpoint. The endpoint returns a list of all subscribers with their details, including email, subscription date, active status, and unsubscribe token."

  - task: "SMTP-Konfiguration: GET/POST/PUT /api/admin/newsletter/smtp"
    implemented: true
    working: false
    file: "/app/backend/server.py"
    stuck_count: 1
    priority: "high"
    needs_retesting: false
    status_history:
      - working: false
        agent: "testing"
        comment: "GET endpoint works correctly, but POST endpoint returns a 500 Internal Server Error. The error occurs when trying to create a new SMTP configuration. This suggests an issue with the implementation of the SMTP configuration creation logic."

  - task: "Newsletter-Vorlagen: GET/POST /api/admin/newsletter/templates"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested newsletter templates endpoints. GET returns a list of all templates, and POST creates a new template with name, subject, and content. The created template is properly stored in the database and returned in subsequent GET requests."

  - task: "Newsletter-Kampagnen: GET/POST /api/admin/newsletter/campaigns"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested newsletter campaigns endpoints. GET returns a list of all campaigns, and POST creates a new campaign with subject, content, and optional template ID. The created campaign is properly stored in the database with a 'draft' status and returned in subsequent GET requests."

  - task: "SMTP-Test: POST /api/admin/newsletter/smtp/test"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "The SMTP test endpoint is implemented correctly. It returns a 400 Bad Request with a message indicating that no SMTP configuration was found, which is expected since we couldn't create a configuration due to the issue with the POST /api/admin/newsletter/smtp endpoint."

  - task: "Menu-System (GET /api/menu/items)"
    implemented: true
    working: false
    file: "/app/backend/server.py"
    stuck_count: 1
    priority: "high"
    needs_retesting: false
    status_history:
      - working: false
        agent: "testing"
        comment: "The GET /api/menu/items endpoint returns a 500 Internal Server Error. The error is due to a data type mismatch: the price field is expected to be a string but some items in the database have it as a float. This suggests a database migration issue where the data format doesn't match the model definition."

  - task: "Menu-System (POST /api/menu/items)"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested creating new menu items. The endpoint accepts all required fields (name, description, price, category) and optional fields (image, details, dietary flags). The created item is properly stored in the database with the correct data types."

  - task: "Menu-System (PUT /api/menu/items/{id})"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested updating menu items. The endpoint accepts partial updates with only the fields that need to be changed. The updated item is properly stored in the database with the correct data types and the updated_at timestamp is updated."

  - task: "Menu-System (DELETE /api/menu/items/{id})"
    implemented: true
    working: true
    file: "/app/backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "testing"
        comment: "Successfully tested deleting menu items. The endpoint marks the item as inactive (is_active=false) rather than actually deleting it from the database, which is the expected behavior. The endpoint returns a success message when the operation is completed."