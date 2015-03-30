__author__ = 'pavel'

from reducer import print_cats

if __name__ == "__main__":

    print_cats(2, {'egov.kz': 3, 'makler.md': 2})
    print_cats(2, {'egov.kz': 1, 'makler.md': 1})
    print_cats(2, {'egov.kz': 3})
    print_cats(2, {'egov.kz': 3, 'makler.md': 1, 'snowmobile.ru': 4, 'mobyware.ru': 1})