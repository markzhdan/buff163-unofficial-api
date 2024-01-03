# Buff163 Unofficial API Wrapper

An unofficial Python API wrapper for Buff163, a CS skin marketplace.

<!-- GETTING STARTED -->

## Installation

Install the package with npm

```sh
pip install buff163-unofficial-api
```

<!-- USAGE EXAMPLES -->

## Usage/Examples

Example of using the API to get frontpage items.

```python
from buff163_unofficial_api import Buff163API

# Example cookie format
[How to get cookie](#installation)
cookie = "Device-Id=_; Locale-Supported=_; game=_; NTES_YD_SESS=_; S_INFO=_; P_INFO=_; remember_me=_; session=_; csrf_token=_"

buff163api = Buff163API(session_cookie=cookie)

market = buff163api.get_featured_market()

for item in market:
    print(f"{item.market_hash_name}")
    print(f"¥ {item.sell_min_price}\n")
```

<!-- CONTRIBUTING -->

## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better or see a missing route, please fork the repo and create a pull request. You can also simply open an issue with the tag "contribution". Thanks for taking the time to improve this API wrapper!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See LICENSE.md for more information.

<!-- CONTACT -->

## Contact

Mark Zhdan - markzhdan@gmail.com

Project Link: [https://github.com/markzhdan/buff163-unofficial-api](https://github.com/markzhdan/buff163-unofficial-api)

PyPI Link: [https://pypi.org/project/buff163-unofficial-api](https://pypi.org/project/buff163-unofficial-api/)
