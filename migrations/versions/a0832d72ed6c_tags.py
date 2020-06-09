"""Tags

Revision ID: a0832d72ed6c
Revises: d67aef2d2e54
Create Date: 2020-06-09 14:35:27.878692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0832d72ed6c'
down_revision = 'd67aef2d2e54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tag_name'), ['name'], unique=False)

    op.create_table('article_tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'article_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tags')
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tag_name'))

    op.drop_table('tag')
    # ### end Alembic commands ###