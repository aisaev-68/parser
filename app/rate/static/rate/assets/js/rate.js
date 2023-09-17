var mix = {
  methods: {
    setSort(id) {
      if (this.selectedSort?.id === id) {
        this.selectedSort.selected =
          this.selectedSort.selected === 'dec' ? 'inc' : 'dec';
      } else {
        if (this.selectedSort) {
          this.selectedSort = null;
        }
        this.selectedSort = this.sortRules.find((sort) => sort.id === id);
        this.selectedSort = {
          ...this.selectedSort,
          selected: 'dec',
        };
      }
      //alert(Object.values(this.selectedSort))
      this.getRates();
    },
    getRates(page) {
      if (typeof page === 'undefined') {
        page = 1;
      }
      const PAGE_LIMIT = 6;

      const params = new URLSearchParams(window.location.search);

      // Установка параметров запроса в адресной строке
      params.set('page', page.toString());

      if (this.selectedSort) {
        params.set('sort', this.selectedSort.id);
        params.set('sortType', this.selectedSort.selected);
      }

      if (this.filter.name) {
        params.set('filter.name', this.filter.name);
      }
      if (this.filter.minPrice) {
        params.set('filter.minPrice', this.filter.minPrice.toString());
      }
      if (this.filter.maxPrice) {
        params.set('filter.maxPrice', this.filter.maxPrice.toString());
      }

      this.getData('/api/rates/', {
        page,
        sort: this.selectedSort ? this.selectedSort.id : null,
        sortType: this.selectedSort ? this.selectedSort.selected : null,
        filter: {
          name: this.filter.name ? this.filter.name : null,
          minPrice: this.filter.minPrice ? this.filter.minPrice : null,
          maxPrice: this.filter.maxPrice ? this.filter.maxPrice : null,
        },
        limit: PAGE_LIMIT,
      })
        .then((data) => {
          this.ratesCards = data.items;
          this.currentPage = data.currentPage;
          this.lastPage = data.lastPage;

          // Обновление адресной строки
          window.history.replaceState(null, null, '?' + params.toString());
          this.resetFilters();
          //this.updateURL();
        })
        .catch(() => {
          console.warn('Ошибка при получении услуг');
        });
    },

    resetFilters() {
        this.filter = {
          name: '',
          minPrice: 1,
          maxPrice: 6000,
        };
    },
      updateFilterPrice(data) {
      // data - объект с полями from и to, содержащими текущие значения ползунка
      this.filter.minPrice = data.from;
      this.filter.maxPrice = data.to;
    },
    initRangeSlider() {
      var $range = $('.range'),
        $line = $range.find('.range-line');

      $line.ionRangeSlider({
        onStart: function (data) {
          $('.rangePrice').text('₽' + data.from + ' - ₽' + data.to);
        },
        onChange: (data) => {
          $('.rangePrice').text('₽' + data.from + ' - ₽' + data.to);
          this.updateFilterPrice(data);
        },
      });
    },


    },
    mounted() {
    this.initRangeSlider();
    const urlParams = new URL(window.location.href).searchParams;
//    this.selectedSort = this.sortRules.find((sort) => sort.id === 'price');
//    this.selectedSort.selected = 'inc';
//    this.getRates(1);
        if (!this.selectedSort) {
            this.selectedSort = this.sortRules.find((sort) => sort.id === 'price');
            if (this.selectedSort) {
              this.selectedSort.selected = 'inc';
            }
          }

  // Убедимся, что this.selectedSort не является null перед вызовом getRates
  if (this.selectedSort) {
    this.getRates(1);
  }
  },
  data() {
    return {
      pages: 1,
      ratesCards: [],
      currentPage: null,
      lastPage: 1,
      selectedSort: null,
      filter: {
        name: '',
        minPrice: 1,
        maxPrice: 6000,
      },
      filters: {
          price: {
            minValue: 1,
            maxValue: 10000,
            currentFromValue: 1,
            currentToValue: 6000
          }
        },
        sortRules: [
          { id: 'card_title', title: 'Тарифному плану' },
          { id: 'price_main', title: 'Цене' },
        ],
      currentURL: window.location.href,

    };
  },
};

