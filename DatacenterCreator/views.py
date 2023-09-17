from django.shortcuts import render
from datetime import date

# Create your views here.
collection = {'data':
    {
        'current_date': date.today(),
        'orders': [
            {'title': 'Intel core i5-15600k', 'id': 1, 'price': 50000,
             'img': 'Intel_Core_i5_2020_logo.svg'},
            {'title': 'Intel core i7-17700k', 'id': 2, 'price': 90000,
             'img': 'Intel_Core_i7_2020_logo.svg.png'},
            {'title': 'Intel core i9-19900k', 'id': 3, 'price': 160000,
             'img': 'Intel_Core_i9_2020_logo.svg.png'},
            {'title': 'Samsung SSD 990 Pro 2TB', 'id': 4, 'price': 30000,
             'img': 'nakopitel_ssd_samsung_m.2_990_pro_2tb_pcie_4.0_x4_v_nand_tlc_mz_v9p2t0bw__2382201_1.jpg'},
            {'title': 'Kingston Fury DDR5 4x32GB', 'id': 5, 'price': 30000,
             'img': 'kingston_fury_beast_ddr5_4x32gb_kf552c40bbk4_128_1.jpg'},
            {'title': 'RTX A100', 'id': 6, 'price': 10000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'RTX A40', 'id': 7, 'price': 5000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'Intel core i5-15600k', 'id': 8, 'price': 50000,
             'img': 'Intel_Core_i5_2020_logo.svg'},
            {'title': 'Intel core i7-17700k', 'id': 9, 'price': 90000,
             'img': 'Intel_Core_i7_2020_logo.svg.png'},
            {'title': 'Intel core i7-19900k', 'id': 10, 'price': 160000,
             'img': 'Intel_Core_i9_2020_logo.svg.png'},
            {'title': 'Samsung SSD 990 Pro 2TB', 'id': 11, 'price': 30000,
             'img': 'nakopitel_ssd_samsung_m.2_990_pro_2tb_pcie_4.0_x4_v_nand_tlc_mz_v9p2t0bw__2382201_1.jpg'},
            {'title': 'Kingston Fury DDR5 4x32GB', 'id': 12, 'price': 30000,
             'img': 'kingston_fury_beast_ddr5_4x32gb_kf552c40bbk4_128_1.jpg'},
            {'title': 'RTX A100', 'id': 13, 'price': 10000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'RTX A40', 'id': 14, 'price': 5000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'Intel core i5-15600k', 'id': 15, 'price': 50000,
             'img': 'Intel_Core_i5_2020_logo.svg'},
            {'title': 'Intel core i7-17700k', 'id': 16, 'price': 90000,
             'img': 'Intel_Core_i7_2020_logo.svg.png'},
            {'title': 'Intel core i9-19900k', 'id': 17, 'price': 160000,
             'img': 'Intel_Core_i9_2020_logo.svg.png'},
            {'title': 'Samsung SSD 990 Pro 2TB', 'id': 18, 'price': 30000,
             'img': 'nakopitel_ssd_samsung_m.2_990_pro_2tb_pcie_4.0_x4_v_nand_tlc_mz_v9p2t0bw__2382201_1.jpg'},
            {'title': 'Kingston Fury DDR5 4x32GB', 'id': 19, 'price': 30000,
             'img': 'kingston_fury_beast_ddr5_4x32gb_kf552c40bbk4_128_1.jpg'},
            {'title': 'RTX A100', 'id': 20, 'price': 10000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'RTX A40', 'id': 21, 'price': 5000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'Intel core i5-15600k', 'id': 22, 'price': 50000,
             'img': 'Intel_Core_i5_2020_logo.svg'},
            {'title': 'Intel core i7-17700k', 'id': 23, 'price': 90000,
             'img': 'Intel_Core_i7_2020_logo.svg.png'},
            {'title': 'Intel core i9-19900k', 'id': 24, 'price': 160000,
             'img': 'Intel_Core_i9_2020_logo.svg.png'},
            {'title': 'Samsung SSD 990 Pro 2TB', 'id': 25, 'price': 30000,
             'img': 'nakopitel_ssd_samsung_m.2_990_pro_2tb_pcie_4.0_x4_v_nand_tlc_mz_v9p2t0bw__2382201_1.jpg'},
            {'title': 'Kingston Fury DDR5 4x32GB', 'id': 26, 'price': 30000,
             'img': 'kingston_fury_beast_ddr5_4x32gb_kf552c40bbk4_128_1.jpg'},
            {'title': 'RTX A100', 'id': 27, 'price': 10000000,
             'img': 'LD0005894794_1.jpg'},
            {'title': 'RTX A40', 'id': 28, 'price': 5000000,
             'img': 'LD0005894794_1.jpg'},
        ],
        'empty': {'title': 'Ничего не найдено', 'id': -1, 'price': 0,
                  'img': '1640100328_2-abrakadabra-fun-p-neitralnii-fon-dlya-afishi-2.jpg'},

    }}


def GetOrders(request):
    return render(request, 'orders.html', collection)


def GetOrder(request, id):
    print({'data':
        {
            'current_date': date.today(),
            'orders':
                filter(lambda dict: id == dict['id'], collection['data'].get('orders')),
            'empty': {'title': 'Ничего не найдено', 'id': 9999, 'price': 0},
        }
    })
    return render(request,
                  'order.html',
                  {'data':
                      {
                          'current_date': date.today(),
                          'orders':
                              filter(lambda dict: id == dict['id'], collection['data'].get('orders')),
                          'empty': {'title': 'Ничего не найдено', 'id': 9999, 'price': 0},
                      }
                  })


def sendText(request):
    input_text = request.POST['text']
    return render(request,
                  'orders.html',
                  {'data':
                      {
                          'current_date': date.today(),
                          'orders':
                              filter(lambda dict: input_text in dict['title'], collection['data'].get('orders')),
                          'empty': {'title': 'Ничего не найдено', 'id': 9999, 'price': 0},
                      }
                  }
                  )
