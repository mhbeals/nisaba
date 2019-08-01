# Nisaba 0.2.8
A tool for multi-modal annotation

## Most Recent Update

### v.0.2.8

+ Minor fixes to get pip install working on Windows

[Full Change Log](changelog.md)

## Install & run instructions

Nisaba is on [PyPi](https://pypi.org/project/nisaba/) so the easiest way to install it is by using pip:

```
pip install nisaba
```

Then just do from your terminal:

```
nisaba
```

## Contributing

If you want to run Nisaba directly from source:

```
git clone https://github.com/mhbeals/nisaba
cd nisaba
virtualenv .
source bin/activate
pip install -r requirements.txt
```

And to run it, just do:

```
cd nisaba
python __main__.py
```

Or just:

```
python -m nisaba
```

## Development History
Conceived by [M. H. Beals](https://github.com/mhbeals) (Loughborough University) and Olivia Mitchell (Loughborough University)  
Initial Development (0.1.0) by [M. H. Beals](https://github.com/mhbeals)  
Continuing Development by [M. H. Beals](https://github.com/mhbeals) and [Albert Meroño Peñuela](https://github.com/albertmeronyo) (Vrije Universiteit Amsterdam)  

## Dependencies
- [rdflib](https://github.com/RDFLib/rdflib)
- [ttkwidgets](https://github.com/RedFantom/ttkwidgets)
