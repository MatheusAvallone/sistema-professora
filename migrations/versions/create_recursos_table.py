"""create recursos table

Revision ID: create_recursos_table
Revises: create_planos_aula
Create Date: 2024-03-19 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_recursos_table'
down_revision = 'create_planos_aula'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('recursos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('url', sa.String(length=255), nullable=True),
        sa.Column('arquivo_path', sa.String(length=255), nullable=True),
        sa.Column('disciplina', sa.String(length=50), nullable=True),
        sa.Column('serie', sa.String(length=20), nullable=True),
        sa.Column('tags', sa.String(length=200), nullable=True),
        sa.Column('professor_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['professor_id'], ['professoras.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recursos_professor_id'), 'recursos', ['professor_id'], unique=False)
    op.create_index(op.f('ix_recursos_tipo'), 'recursos', ['tipo'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_recursos_tipo'), table_name='recursos')
    op.drop_index(op.f('ix_recursos_professor_id'), table_name='recursos')
    op.drop_table('recursos') 