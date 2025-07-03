from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9b53a3c8dbdb'
down_revision = 'd53ea4a6bd32'
branch_labels = None
depends_on = None

# Define enum
user_role_enum = postgresql.ENUM('USER', 'ADMIN', 'SUPERUSER', name='user_role_enum')

def upgrade():
    # Create enum type in DB
    user_role_enum.create(op.get_bind())

    # Alter column with USING clause for casting
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE user_role_enum USING role::user_role_enum")

def downgrade():
    # Revert column to VARCHAR first
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR(50)")

    # Drop enum type
    user_role_enum.drop(op.get_bind())
