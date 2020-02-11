"""Fixture - all fields nullable except url

Revision ID: 272a82bce47d
Revises: a0cf9ae7d05f
Create Date: 2020-02-03 17:31:57.003704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272a82bce47d'
down_revision = 'a0cf9ae7d05f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fixtures', schema=None) as batch_op:
        batch_op.alter_column('competition',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('country',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('team_a',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('team_b',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fixtures', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('team_b',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('team_a',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('country',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('competition',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###