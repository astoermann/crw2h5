# Linux Optional Commands


```{note}
These documents will not go in depth for these commands since they are optional and it is assumed you know how to do use Kutas Lab commands already. If you need help, see the Kutas Lab Pipeline training documents
```

## Create an .x.log 

x.log should be created if the data has already been screened for artifacts using the Kutas Lab software (garv)

Copy the log file to a working copy (named .x.log)

```
cp stm02.log stm02.x.log 
```

Create a bin list file (blf) for use in avg 

```
cdbl stmath.bdf stm02.x.log stm02.blf 250
```

Use the '-x' option in avg 

```
echo stm02.crw stm02.x.log stm02.blf | avg 100 stm02.avg -a stm02.arf -x 
```
