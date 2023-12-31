from django.db import models

class Usuario(models.Model):
    tipoid = models.CharField( max_length=2)  # The composite primary key (tipoid, numid) found, that is not supported. The first column is selected.
    numid = models.DecimalField(max_digits=10, decimal_places=0, primary_key=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    genero = models.CharField(max_length=1)
    correo = models.CharField(max_length=30)
    usuario = models.CharField(max_length=30)
    contrasena = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'usuario'
        unique_together = (('tipoid', 'numid'),)

class Admin(models.Model):
    tipoidusuario = models.CharField(max_length=2)  # The composite primary key (tipoidusuario, numidusuario) found, that is not supported. The first column is selected.
    numidusuario = models.OneToOneField('Usuario', models.DO_NOTHING,db_column='numidusuario', primary_key=True)

    class Meta:
        managed = False
        db_table = 'admin'
        unique_together = (('tipoidusuario', 'numidusuario'),)


class Artista(models.Model):
    tipoidusuario = models.CharField(max_length=2)  # The composite primary key (tipoidusuario, numidusuario) found, that is not supported. The first column is selected.
    numidusuario = models.OneToOneField(Usuario, models.DO_NOTHING,db_column='numidusuario', primary_key=True)
    utilidad = models.DecimalField(max_digits=8, decimal_places=2)
    numventas = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'artista'
        unique_together = (('tipoidusuario', 'numidusuario'),)


class Camiseta(models.Model):
    idcamiseta = models.CharField(primary_key=True, max_length=5)
    talla = models.CharField(max_length=2)
    color = models.CharField(max_length=15)
    material = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=6, decimal_places=0)
    imgurl = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'camiseta'


class Catalogocamiseta(models.Model):
    idcatcamiseta = models.CharField(primary_key=True, max_length=5)
    idcamiseta = models.ForeignKey(Camiseta, models.DO_NOTHING, db_column='idcamiseta')
    cantdisponible = models.DecimalField(max_digits=3, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'catalogocamiseta'


class Catalogoestampa(models.Model):
    idcatestampa = models.CharField(primary_key=True, max_length=5)
    idestampa = models.ForeignKey('Estampa', models.DO_NOTHING, db_column='idestampa')
    cantdisponible = models.DecimalField(max_digits=3, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'catalogoestampa'


class Cliente(models.Model):
    tipoidusuario = models.CharField(max_length=2)  # The composite primary key (tipoidusuario, numidusuario) found, that is not supported. The first column is selected.
    numidusuario = models.OneToOneField('Usuario', models.DO_NOTHING,db_column='numidusuario', primary_key=True)
    direccion = models.CharField(max_length=30)
    

    class Meta:
        managed = False
        db_table = 'cliente'
        unique_together = (('tipoidusuario', 'numidusuario'),)


class Estampa(models.Model):
    idestampa = models.CharField(primary_key=True, max_length=5)
    nombre = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=200)
    imgurl = models.CharField(max_length=200)
    disponible = models.BooleanField()
    tema = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=6, decimal_places=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    tipoidartista = models.CharField(max_length=2)
    #tipoidartista = models.ForeignKey(Artista, models.DO_NOTHING, db_column='tipoidartista')
    numidartista = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'estampa'


class Factura(models.Model):
    idfactura = models.CharField(primary_key=True, max_length=5)
    tipoidcliente = models.CharField(max_length=3)
    numidcliente = models.DecimalField(max_digits=10, decimal_places=0)
    idcamiseta = models.ForeignKey(Camiseta, models.DO_NOTHING, db_column='idcamiseta')
    idestampa = models.ForeignKey(Estampa, models.DO_NOTHING, db_column='idestampa')
    preciototal = models.DecimalField(max_digits=7, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'factura'



