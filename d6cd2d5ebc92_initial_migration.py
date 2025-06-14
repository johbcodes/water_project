from alembic import op
import sqlalchemy as sa

def upgrade():
    # Check if the table already exists
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table('Counties'):
        op.create_table(
            'Counties',
            sa.Column('CountyID', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('CountyName', sa.String(100), nullable=False)
        )