"""create planos aula table

Revision ID: create_planos_aula
Revises: create_calendario_tables
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_planos_aula'
down_revision = 'create_calendario_tables'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('planos_aula',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(length=100), nullable=False),
        sa.Column('disciplina', sa.String(length=50), nullable=False),
        sa.Column('serie', sa.String(length=20), nullable=False),
        sa.Column('data_aula', sa.Date(), nullable=False),
        sa.Column('duracao', sa.Integer(), nullable=False),
        sa.Column('objetivos', sa.Text(), nullable=False),
        sa.Column('conteudo', sa.Text(), nullable=False),
        sa.Column('metodologia', sa.Text(), nullable=False),
        sa.Column('recursos', sa.Text(), nullable=False),
        sa.Column('avaliacao', sa.Text(), nullable=False),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='Pendente'),
        sa.Column('professor_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['professor_id'], ['professoras.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_planos_aula_data_aula'), 'planos_aula', ['data_aula'], unique=False)
    op.create_index(op.f('ix_planos_aula_professor_id'), 'planos_aula', ['professor_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_planos_aula_professor_id'), table_name='planos_aula')
    op.drop_index(op.f('ix_planos_aula_data_aula'), table_name='planos_aula')
    op.drop_table('planos_aula') 