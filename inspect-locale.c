#include <stdio.h>
#include <locale.h>
#include <wchar.h>
#include <wctype.h>


void print_bytes(const wchar_t *s)
{
    for (size_t i = 0; i < wcslen(s); ++i) {
        wprintf(L"\\x%02x", (wint_t)s[i]);
    }
    wprintf(L"\n");
}


void perform_test()
{
    const wchar_t *in1 = L"a";
    wchar_t out1[1+wcsxfrm(NULL, in1, 0)];
    wcsxfrm(out1, in1, sizeof out1);

    const wchar_t *in2 = L"A";
    wchar_t out2[1+wcsxfrm(NULL, in2, 0)];
    wcsxfrm(out2, in2, sizeof out2);

    const wchar_t *in3 = L"apple";
    wchar_t out3[1+wcsxfrm(NULL, in3, 0)];
    wcsxfrm(out3, in3, sizeof out3);

    const wchar_t *in4 = L"Apple";
    wchar_t out4[1+wcsxfrm(NULL, in4, 0)];
    wcsxfrm(out4, in4, sizeof out4);

    print_bytes(out1);
    print_bytes(out2);
    print_bytes(out3);
    print_bytes(out4);

    printf("Comparisons:\n");
    int cmp1 = wcscmp(out1, out2);
    int cmp2 = wcscmp(out3, out4);
    printf("wcscmp(out1, out2) = %d\n", cmp1);
    printf("wcscmp(out3, out4) = %d\n", cmp2);
}


int main()
{
    setlocale(LC_ALL, "C");
    printf("Locale: %s\n", setlocale(LC_ALL, NULL));
    perform_test();

    setlocale(LC_ALL, "en_US.UTF-8");
    printf("Locale: %s\n", setlocale(LC_ALL, NULL));
    perform_test();
}
