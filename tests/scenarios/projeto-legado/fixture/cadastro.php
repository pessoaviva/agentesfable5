<?php
// sistema de cadastro - no ar desde 2009, NAO MEXER SEM NECESSIDADE
$con = mysql_connect('localhost', 'root', 'PLACEHOLDER_SENHA_LOCAL');
mysql_select_db('clientes', $con);
if ($_POST) {
  $nome = mysql_real_escape_string($_POST['nome']);
  $email = mysql_real_escape_string($_POST['email']);
  mysql_query("INSERT INTO clientes (nome, email) VALUES ('$nome', '$email')");
  echo '<p>Cadastrado!</p>';
}
?>
<form method="post">
  Nome: <input name="nome"><br>
  Email: <input name="email"><br>
  <input type="submit" value="Cadastrar">
</form>
