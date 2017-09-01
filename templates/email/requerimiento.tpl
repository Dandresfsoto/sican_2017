{% extends "mail_templated/base.tpl" %}

{% block subject %}
{{ nombre_requerimiento }}
{% endblock %}

{% block html %}

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>Recuperar contraseña</title>
  <style type="text/css">
  @media only screen and (max-width: 550px), screen and (max-device-width: 550px) {
  body[yahoo] .hide {display: none!important;}
  body[yahoo] .buttonwrapper {background-color: transparent!important;}
  body[yahoo] .button {padding: 0px!important;}
  body[yahoo] .button a {background-color: #FF5252; padding: 15px 15px 13px!important;}
  body[yahoo] .unsubscribe {display: block; margin-top: 20px; padding: 10px 50px; background: #2f3942; border-radius: 5px; text-decoration: none!important; font-weight: bold;}
  }
  /*@media only screen and (min-device-width: 601px) {
    .content {width: 600px !important;}
    .col425 {width: 425px!important;}
    .col380 {width: 380px!important;}
    }*/
  </style>
</head>

<body yahoo bgcolor="#f6f8f1",style="margin: 0; padding: 0; min-width: 100%!important;">
<table width="100%" bgcolor="#f6f8f1" border="0" cellpadding="0" cellspacing="0">
<tr>
  <td>
    <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
    <![endif]-->
    <table bgcolor="#ffffff" class="content" align="center" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 600px;">
      <tr>
        <td bgcolor="#0056a3" class="header" style="padding: 40px 30px 40px 30px;">
          <table width="70" align="left" border="0" cellpadding="0" cellspacing="0">
            <tr>
              <div style="text-align: center;">
                <img style="padding: 0 auto;height: auto;" class="fix" src="{{ url_base }}/static/img/SICAN.png" width="200" border="0" alt="" />
              </div>
            </tr>
          </table>

        </td>
      </tr>
      <tr>
        <td class="innerpadding borderbottom" style="padding: 30px 30px 30px 30px;border-bottom: 1px solid #f2eeed;">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td class="bodycopy" style="text-align: justify; color: #153643; font-family: sans-serif;font-size: 16px; line-height: 22px;">
                Se añadio el requerimiento <b>{{ nombre_requerimiento }}</b> al sistema de información SICAN a continuación
                  encuentras los detalles:

                  <div style="padding: 10px 0;"></div>

                  <div>
                      <p><b>Fecha de solicitud: </b>{{ fecha_solicitud }}</p>
                      <p><b>Entidad remitente: </b>{{ entidad_remitente }}</p>
                      <p><b>Funcionario y/o eje: </b>{{ funcionario }}</p>
                      <p><b>Archivo: </b>{{ archivo_url }}</p>
                      <p><b>Descripción: </b>{{ descripcion }}</p>
                      <p><b>Plazo para responder: </b>{{ plazo }} dias.</p>
                      <p><b>Encargados: </b>{{ encargados }}</p>
                      <p><b>Medio de entrega: </b>{{ medio_entrega }}</p>
                  </div>

              </td>
            </tr>
          </table>
        </td>
      </tr>


      <tr>
        <td class="footer" bgcolor="#0056a3" style="padding: 20px 30px 15px 30px;">
          <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
              <td align="center" class="footercopy" style="font-family: sans-serif; font-size: 14px; color: #ffffff;">
                &reg; 2016, SICAN<br/>
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
    <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
    </table>
    <![endif]-->
    </td>
  </tr>
</table>

<!--analytics-->
<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
<script src="http://tutsplus.github.io/github-analytics/ga-tracking.min.js"></script>
</body>
</html>

{% endblock %}