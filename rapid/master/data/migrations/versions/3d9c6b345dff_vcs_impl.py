"""
 Copyright (c) 2015 Michael Bright and Bamboo HR LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

vcs_impl

Revision ID: 3d9c6b345dff
Revises: 9e49690a25da
Create Date: 2016-02-01 11:43:43.657842

"""

# revision identifiers, used by Alembic.

revision = '3d9c6b345dff'
down_revision = '9e49690a25da'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('integration_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_integration_keys_id'), 'integration_keys', ['id'], unique=False)
    op.create_table('integration_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_integration_types_id'), 'integration_types', ['id'], unique=False)
    op.create_table('vcs_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_vcs_types_id'), 'vcs_types', ['id'], unique=False)
    op.create_table('integrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('integration_type_id', sa.Integer(), nullable=False),
    sa.Column('integration_keys_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['integration_keys_id'], ['integration_keys.id'], ),
    sa.ForeignKeyConstraint(['integration_type_id'], ['integration_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_integrations_id'), 'integrations', ['id'], unique=False)
    op.create_table('vcs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1500), nullable=False),
    sa.Column('repo', sa.String(length=500), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('vcs_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vcs_type_id'], ['vcs_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_vcs_id'), 'vcs', ['id'], unique=False)
    op.create_table('commits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commit_identifier', sa.String(length=255), nullable=False),
    sa.Column('vcs_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vcs_id'], ['vcs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_commits_commit_identifier'), 'commits', ['commit_identifier'], unique=False)
    op.create_index(op.f('ix_commits_id'), 'commits', ['id'], unique=False)
    op.create_index(op.f('ix_commits_vcs_id'), 'commits', ['vcs_id'], unique=False)
    op.create_table('commit_integrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commit_id', sa.Integer(), nullable=False),
    sa.Column('integration_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['commit_id'], ['commits.id'], ),
    sa.ForeignKeyConstraint(['integration_id'], ['integrations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_commit_integrations_commit_id'), 'commit_integrations', ['commit_id'], unique=False)
    op.create_index(op.f('ix_commit_integrations_id'), 'commit_integrations', ['id'], unique=False)
    op.create_index(op.f('ix_commit_integrations_integration_id'), 'commit_integrations', ['integration_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_commit_integrations_integration_id'), table_name='commit_integrations')
    op.drop_index(op.f('ix_commit_integrations_id'), table_name='commit_integrations')
    op.drop_index(op.f('ix_commit_integrations_commit_id'), table_name='commit_integrations')
    op.drop_table('commit_integrations')
    op.drop_index(op.f('ix_commits_vcs_id'), table_name='commits')
    op.drop_index(op.f('ix_commits_id'), table_name='commits')
    op.drop_index(op.f('ix_commits_commit_identifier'), table_name='commits')
    op.drop_table('commits')
    op.drop_index(op.f('ix_vcs_id'), table_name='vcs')
    op.drop_table('vcs')
    op.drop_index(op.f('ix_integrations_id'), table_name='integrations')
    op.drop_table('integrations')
    op.drop_index(op.f('ix_vcs_types_id'), table_name='vcs_types')
    op.drop_table('vcs_types')
    op.drop_index(op.f('ix_integration_types_id'), table_name='integration_types')
    op.drop_table('integration_types')
    op.drop_index(op.f('ix_integration_keys_id'), table_name='integration_keys')
    op.drop_table('integration_keys')
    ### end Alembic commands ###
