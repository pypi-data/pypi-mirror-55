def get_absolute_return (invested_amount, current_amount, duration):
    profit =  current_amount - invested_amount
    return profit/(invested_amount*duration)*100


def test_check_get_absolute_return():
    print(get_absolute_return(100, 100, 2))
    if get_absolute_return(100, 110, 2) == 5.0 :
        print("successful")
    else:
        print("failed")