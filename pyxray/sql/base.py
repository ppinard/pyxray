""""""

# Standard library modules.
import collections

# Third party modules.

# Local modules.
from pyxray.base import NotFound
import pyxray.descriptor as descriptor
from pyxray.sql.command import SelectBuilder

# Globals and constants variables.

class SqlDatabaseMixin:

    def _select_element(self, connection, builder, table, column, element):
        if hasattr(element, 'atomic_number'):
            element = element.atomic_number

        if isinstance(element, str):
            builder.add_join('element_name', 'element_id', table, column)
            builder.add_join('element_symbol', 'element_id', table, column)
            builder.add_where('element_name', 'name', '=', element,
                              'element_symbol', 'symbol', '=', element)

        elif isinstance(element, int):
            builder.add_join('element', 'id', table, column)
            builder.add_where('element', 'atomic_number', '=', element)

        else:
            raise NotFound('Cannot parse element: {}'.format(element))

    def _select_atomic_shell(self, connection, builder, table, column, atomic_shell):
        if hasattr(atomic_shell, 'principal_quantum_number'):
            atomic_shell = atomic_shell.principal_quantum_number

        if isinstance(atomic_shell, str):
            builder.add_join('atomic_shell_notation', 'atomic_shell_id', table, column)
            builder.add_where('atomic_shell_notation', 'ascii', '=', atomic_shell,
                              'atomic_shell_notation', 'utf16', '=', atomic_shell)

        elif isinstance(atomic_shell, int):
            builder.add_join('atomic_shell', 'id', table, column)
            builder.add_where('atomic_shell', 'principal_quantum_number', '=', atomic_shell)

        else:
            raise NotFound('Cannot parse atomic shell: {}'.format(atomic_shell))

    def _expand_atomic_subshell(self, atomic_subshell):
        n = 0
        l = -1
        j_n = 0
        if hasattr(atomic_subshell, 'principal_quantum_number') and \
                hasattr(atomic_subshell, 'azimuthal_quantum_number') and \
                hasattr(atomic_subshell, 'total_angular_momentum_nominator'):
            n = atomic_subshell.atomic_shell.principal_quantum_number
            l = atomic_subshell.azimuthal_quantum_number
            j_n = atomic_subshell.total_angular_momentum_nominator

        elif isinstance(atomic_subshell, collections.Sequence) and \
                len(atomic_subshell) == 3:
            n = atomic_subshell[0]
            l = atomic_subshell[1]
            j_n = atomic_subshell[2]

        return n, l, j_n

    def _select_atomic_subshell(self, connection, builder, table, column, atomic_subshell):
        n, l, j_n = self._expand_atomic_subshell(atomic_subshell)

        builder.add_join('atomic_subshell', 'id', table, column)
        builder.add_join('atomic_shell', 'id', 'atomic_subshell', 'atomic_shell_id')

        if isinstance(atomic_subshell, str):
            builder.add_join('atomic_subshell_notation', 'atomic_subshell_id', table, column)
            builder.add_where('atomic_subshell_notation', 'ascii', '=', atomic_subshell,
                              'atomic_subshell_notation', 'utf16', '=', atomic_subshell)

        elif n > 0 and l >= 0 and j_n > 0:
            builder.add_where('atomic_shell', 'principal_quantum_number', '=', n)
            builder.add_where('atomic_subshell', 'azimuthal_quantum_number', '=', l)
            builder.add_where('atomic_subshell', 'total_angular_momentum_nominator', '=', j_n)

        else:
            raise NotFound('Cannot parse atomic subshell: {}'.format(atomic_subshell))

    def _select_xray_transition(self, connection, builder, table, column, xraytransition):
        src_n = 0; src_l = -1; src_j_n = 0
        dst_n = 0; dst_l = -1; dst_j_n = 0

        if hasattr(xraytransition, 'source_subshell') and \
                hasattr(xraytransition, 'destination_subshell'):
            src_n, src_l, src_j_n = \
                self._expand_atomic_subshell(xraytransition.source_subshell)
            dst_n, dst_l, dst_j_n = \
                self._expand_atomic_subshell(xraytransition.destination_subshell)

        elif isinstance(xraytransition, collections.Sequence) and \
                len(xraytransition) >= 2:
            src_n, src_l, src_j_n = self._expand_atomic_subshell(xraytransition[0])
            dst_n, dst_l, dst_j_n = self._expand_atomic_subshell(xraytransition[1])

        builder.add_join('xray_transition', 'id', table, column)
        builder.add_join('atomic_subshell', 'id', 'xray_transition', 'source_subshell_id', 'srcsubshell')
        builder.add_join('atomic_subshell', 'id', 'xray_transition', 'destination_subshell_id', 'dstsubshell')
        builder.add_join('atomic_shell', 'id', 'srcsubshell', 'atomic_shell_id', 'srcshell')
        builder.add_join('atomic_shell', 'id', 'dstsubshell', 'atomic_shell_id', 'dstshell')

        if isinstance(xraytransition, str):
            builder.add_join('xray_transition_notation', 'xray_transition_id', table, column)
            builder.add_where('xray_transition_notation', 'ascii', '=', xraytransition,
                              'xray_transition_notation', 'utf16', '=', xraytransition)

        elif src_n > 0 and src_l >= 0 and src_j_n > 0 and \
                dst_n > 0 and dst_l >= 0 and dst_j_n > 0:
            builder.add_where('srcshell', 'principal_quantum_number', '=', src_n)
            builder.add_where('srcsubshell', 'azimuthal_quantum_number', '=', src_l)
            builder.add_where('srcsubshell', 'total_angular_momentum_nominator', '=', src_j_n)
            builder.add_where('dstshell', 'principal_quantum_number', '=', dst_n)
            builder.add_where('dstsubshell', 'azimuthal_quantum_number', '=', dst_l)
            builder.add_where('dstsubshell', 'total_angular_momentum_nominator', '=', dst_j_n)

        else:
            raise NotFound('Cannot parse X-ray transition: {}'.format(xraytransition))

    def _select_xray_transitionset(self, connection, builder, table, column, xraytransitionset):
        xraytransitions = set()
        if isinstance(xraytransitionset, descriptor.XrayTransitionSet):
            xraytransitions.update(xraytransitionset.transitions)

        elif isinstance(xraytransitionset, collections.Sequence):
            xraytransitions.update(xraytransitionset)

        if isinstance(xraytransitionset, str):
            builder.add_join('xray_transitionset_notation', 'xray_transitionset_id', table, column)
            builder.add_where('xray_transitionset_notation', 'ascii', '=', xraytransitionset,
                              'xray_transitionset_notation', 'utf16', '=', xraytransitionset)
            return

        elif xraytransitions:
            possibilities = set()
            for i, xraytransition in enumerate(xraytransitions):
                subtable = 'xray_transitionset_association'
                subbuilder = SelectBuilder()
                subbuilder.add_select(subtable, 'xray_transitionset_id')
                subbuilder.add_select('xray_transitionset', 'count')
                subbuilder.add_from(subtable)
                subbuilder.add_join('xray_transitionset', 'id', subtable, 'xray_transitionset_id')
                self._select_xray_transition(connection, subbuilder, subtable, 'id', xraytransition)
                sql, params = subbuilder.build()

                cur = connection.cursor()
                cur.execute(sql, params)
                rows = cur.fetchall()
                cur.close()

                if i == 0:
                    possibilities.update(rows)
                else:
                    possibilities.intersection_update(rows)

                if not possibilities:
                    break

            for xray_transitionset_id, count in possibilities:
                if count == len(xraytransitions):
                    builder.add_join('xray_transitionset', 'id', table, column)
                    builder.add_where('xray_transitionset', 'id', '=', xray_transitionset_id)
                    return

        raise NotFound('Cannot parse X-ray transition set: {}'.format(xraytransitionset))

    def _select_language(self, connection, builder, table, language):
        if isinstance(language, descriptor.Language):
            language = language.code

        builder.add_join('language', 'id', table, 'language_id')
        builder.add_where('language', 'code', '=', language)

    def _select_notation(self, connection, builder, table, notation):
        if isinstance(notation, descriptor.Notation):
            notation = notation.name

        builder.add_join('notation', 'id', table, 'notation_id')
        builder.add_where('notation', 'name', '=', notation)

    def _select_reference(self, connection, builder, table, reference):
        if isinstance(reference, descriptor.Reference):
            reference = reference.bibtexkey

        if reference:
            builder.add_join('ref', 'id', table, 'reference_id')
            builder.add_where('ref', 'bibtexkey', '=', reference)

        else:
            builder.add_orderby(table, 'reference_id')
