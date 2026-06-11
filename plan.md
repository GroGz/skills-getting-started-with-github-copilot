## Plan: Pruebas FastAPI Backend

TL;DR - Añadir pruebas unitarias con `pytest` que cubran los endpoints de inscripción y baja. Usaremos `fastapi.TestClient` y fixtures en `tests/conftest.py` para aislar y restaurar el estado en memoria (`activities`) entre tests.

**Steps**
1. Añadir `pytest` a `requirements.txt` (o crear `requirements-dev.txt`) para poder ejecutar tests. ✅
2. Crear `tests/conftest.py` con:
   - Fixture `client` que importe `app` desde `src.app` y devuelva `TestClient(app)`. ✅
   - Fixture `reset_activities` que haga `deepcopy` de `src.app.activities` antes de cada test y lo restaure después. ✅
3. Crear `tests/test_activities_api.py` con los casos sugeridos: ✅
   - `test_get_activities_returns_all_activities`
   - `test_get_activities_contains_chess_club`
   - `test_signup_new_student_success`
   - `test_signup_for_activity_not_found`
   - `test_signup_duplicate_student_fails`
   - `test_signup_multiple_students_different_activities`
   - `test_unregister_existing_participant_success`
   - `test_unregister_activity_not_found`
   - `test_unregister_participant_not_found`
   - `test_unregister_then_signup_again`
4. Ejecutar `pytest` localmente para verificar todo.
5. (Opcional) Añadir job de CI que instale deps y ejecute `pytest` en pushes/PRs.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot/requirements.txt` — ✅ `pytest` añadido.
- `/workspaces/skills-getting-started-with-github-copilot/src/app.py` — contiene `activities` en memoria; tests restauran su estado.
- `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` — ya existe; configurado para usar.
- `/workspaces/skills-getting-started-with-github-copilot/tests/conftest.py` — ✅ creado con fixtures.
- `/workspaces/skills-getting-started-with-github-copilot/tests/test_activities_api.py` — ✅ creado con AAA pattern.

**Verification**
1. Instalar dependencias de test:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar tests:

   ```bash
   pytest -v
   ```

3. Ejecutar un test concreto para depuración:

   ```bash
   pytest tests/test_activities_api.py::TestSignupForActivity::test_signup_for_activity_success -v
   ```

4. Asegurarse de que los tests se ejecutan aisladamente (no afectan otros tests) gracias a que `reset_activities` restaura el estado.

**Pattern Used**
- **AAA (Arrange-Act-Assert)**: Cada test sigue el patrón:
  - **Arrange**: Preparar los datos y estado necesarios.
  - **Act**: Ejecutar la acción (llamada HTTP).
  - **Assert**: Verificar los resultados esperados.

**Decisions**
- Usaremos `fastapi.TestClient` (sin `pytest-asyncio`) porque los endpoints actuales son sincronizados y `TestClient` simplifica el flujo.
- Restablecer `activities` mediante `deepcopy` en `conftest.py` para evitar fugas de estado entre tests.
- Tests importarán `app` y `activities` desde `src.app` directamente.
- Cada docstring incluye comentarios Arrange/Act/Assert para claridad.

**Further Considerations**
1. Si prefieres pruebas asíncronas con `httpx.AsyncClient`, añadir `pytest-asyncio` y adaptar fixtures.
2. Para mayor consistencia, considerar extraer la construcción de `activities` a una función `get_initial_activities()` en `src/app.py` y reutilizarla en `conftest.py`.
3. Considerar agregar tests para el endpoint `GET /` que redirige a static.
