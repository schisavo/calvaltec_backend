app/
│
├── api/
│   ├── deps/
│   │   ├── auth.py
│   │   ├── permissions.py
│   │   └── company.py
│   │
│   ├── v1/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── companies.py
│   │   ├── evaluations.py
│   │   ├── questions.py
│   │   ├── recommendations.py
│   │   └── reports.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── oauth.py
│   └── exceptions.py
│
├── models/
│   ├── user.py
│   ├── role.py
│   ├── company.py
│   ├── evaluation.py
│   ├── question.py
│   ├── answer.py
│   ├── recommendation.py
│   └── audit_log.py
│
├── schemas/
│   ├── auth.py
│   ├── company.py
│   ├── evaluation.py
│   ├── question.py
│   ├── recommendation.py
│   └── report.py
│
├── repositories/
│   ├── base.py
│   ├── company_repository.py
│   ├── evaluation_repository.py
│   ├── user_repository.py
│   └── question_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── company_service.py
│   ├── evaluation_service.py
│   ├── scoring_service.py
│   ├── recommendation_service.py
│   ├── ai_service.py
│   └── report_service.py
│
├── ai/
│   ├── prompts/
│   │   ├── explain_question.txt
│   │   ├── recommendations.txt
│   │   └── compliance_analysis.txt
│   │
│   └── chains/
│       └── recommendation_chain.py
│
├── utils/
│   ├── enums.py
│   ├── constants.py
│   └── helpers.py
│
├── tests/
│
├── main.py
│
alembic/
│
.env