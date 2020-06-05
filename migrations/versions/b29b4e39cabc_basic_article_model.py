"""basic article model

Revision ID: b29b4e39cabc
Revises: 499ff9f1cd87
Create Date: 2020-06-05 09:50:54.547732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b29b4e39cabc'
down_revision = '499ff9f1cd87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_article_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_article_title'), ['title'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_article_title'))
        batch_op.drop_index(batch_op.f('ix_article_timestamp'))

    op.drop_table('article')
    # ### end Alembic commands ###
