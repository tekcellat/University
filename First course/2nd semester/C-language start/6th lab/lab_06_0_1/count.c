#define SUCCESS 0
#define WRONG_PARAMETERS -1

/* Находит max(a[0] + a[n - 1], a[1] + a[n - 2], ...) целочисленного массива
 * с указателем на начальный элемент p1 и на последний элемент p2 */
int count(const int *pbegin, const int *pend, int *const max)
{
    if (pbegin >= pend)
        return WRONG_PARAMETERS;

    // Присваиваем *max начальное значение
    if (pbegin != pend)
        *max = *pbegin + *pend;
    else
        *max = *pbegin;

    // Основной цикл
    for (; pbegin < pend; pbegin++, pend--)
        if (*pbegin + *pend > *max)
            *max = *pbegin + *pend;

    // Если осталось одно число в середине массива
    if (pbegin == pend && *max < *pend)
        *max = *pend;

    return SUCCESS;
}
