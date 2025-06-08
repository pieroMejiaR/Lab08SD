package bdmysql;

import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.sql.*;

public class Ventana extends JFrame {
    JLabel lblId, lblNombre, lblDescripcion;
    JTextField txtId, txtNombre, txtDescripcion;
    JButton btnPrimero, btnAnterior, btnSiguiente, btnUltimo;
    JButton btnInsertar, btnModificar, btnEliminar, btnActualizar;
    ResultSet resultado;
    Statement sentencia;
    Connection conexion;
    
    public Ventana(String titulo) {
        super(titulo);

        // Etiquetas y campos
        lblId = new JLabel("Id Categoria");
        lblNombre = new JLabel("Nombre");
        lblDescripcion = new JLabel("Descripcion");

        txtId = new JTextField(20);
        txtNombre = new JTextField(20);
        txtDescripcion = new JTextField(20);

        // Botones de navegación
        btnPrimero = new JButton("Primero");
        btnAnterior = new JButton("Anterior");
        btnSiguiente = new JButton("Siguiente");
        btnUltimo = new JButton("Ultimo");

        // Botones de operaciones
        btnInsertar = new JButton("Insertar");
        btnModificar = new JButton("Modificar");
        btnEliminar = new JButton("Eliminar");
        btnActualizar = new JButton("Actualizar");

        // Listeners
        EventoBoton listener = new EventoBoton(this);
        btnPrimero.addActionListener(listener);
        btnAnterior.addActionListener(listener);
        btnSiguiente.addActionListener(listener);
        btnUltimo.addActionListener(listener);
        btnInsertar.addActionListener(listener);
        btnModificar.addActionListener(listener);
        btnEliminar.addActionListener(listener);
        btnActualizar.addActionListener(listener);

        // Panel de etiquetas y campos
        JPanel panelLabels = new JPanel();
        panelLabels.setLayout(new BoxLayout(panelLabels, BoxLayout.Y_AXIS));
        panelLabels.add(lblId);
        panelLabels.add(Box.createRigidArea(new Dimension(0, 10)));
        panelLabels.add(lblNombre);
        panelLabels.add(Box.createRigidArea(new Dimension(0, 10)));
        panelLabels.add(lblDescripcion);

        JPanel panelFields = new JPanel();
        panelFields.setLayout(new BoxLayout(panelFields, BoxLayout.Y_AXIS));
        panelFields.add(txtId);
        panelFields.add(Box.createRigidArea(new Dimension(0, 10)));
        panelFields.add(txtNombre);
        panelFields.add(Box.createRigidArea(new Dimension(0, 10)));
        panelFields.add(txtDescripcion);

        JPanel panelDatos = new JPanel();
        panelDatos.setLayout(new BoxLayout(panelDatos, BoxLayout.X_AXIS));
        panelDatos.add(Box.createRigidArea(new Dimension(10, 10)));
        panelDatos.add(panelLabels);
        panelDatos.add(Box.createRigidArea(new Dimension(10, 10)));
        panelDatos.add(panelFields);

        // Panel de navegación
        JPanel panelNavegacion = new JPanel();
        panelNavegacion.setLayout(new BoxLayout(panelNavegacion, BoxLayout.X_AXIS));
        panelNavegacion.add(btnPrimero);
        panelNavegacion.add(Box.createRigidArea(new Dimension(10, 10)));
        panelNavegacion.add(btnAnterior);
        panelNavegacion.add(Box.createRigidArea(new Dimension(10, 10)));
        panelNavegacion.add(btnSiguiente);
        panelNavegacion.add(Box.createRigidArea(new Dimension(10, 10)));
        panelNavegacion.add(btnUltimo);
        panelNavegacion.setBackground(Color.orange);

        // Panel de operaciones
        JPanel panelOperaciones = new JPanel();
        panelOperaciones.setLayout(new BoxLayout(panelOperaciones, BoxLayout.X_AXIS));
        panelOperaciones.add(btnInsertar);
        panelOperaciones.add(Box.createRigidArea(new Dimension(10, 10)));
        panelOperaciones.add(btnModificar);
        panelOperaciones.add(Box.createRigidArea(new Dimension(10, 10)));
        panelOperaciones.add(btnEliminar);
        panelOperaciones.add(Box.createRigidArea(new Dimension(10, 10)));
        panelOperaciones.add(btnActualizar);
        panelOperaciones.setBackground(Color.blue);

        // Panel principal
        JPanel panelPrincipal = new JPanel();
        panelPrincipal.setLayout(new BoxLayout(panelPrincipal, BoxLayout.Y_AXIS));
        panelPrincipal.add(panelDatos);
        panelPrincipal.add(Box.createRigidArea(new Dimension(0, 20)));
        panelPrincipal.add(panelOperaciones);
        panelPrincipal.add(Box.createRigidArea(new Dimension(0, 20)));
        panelPrincipal.add(panelNavegacion);
        panelPrincipal.setBackground(new Color(255, 0, 0));

        getContentPane().add(panelPrincipal, BorderLayout.CENTER);
        addWindowListener(new EventosVentana(this));

        Conexion();
    }

    private void Conexion() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver").newInstance();
            conexion = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/EmpresaMSQL?useSSL=false&serverTimezone=UTC",
                "root", "admin"
            );
            sentencia = conexion.createStatement(
                ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY
            );
            boolean tieneResultados = sentencia.execute("SELECT * FROM Categorias");
            if (tieneResultados) {
                resultado = sentencia.getResultSet();
                if (resultado != null && resultado.first()) {
                    mostrarResultados(resultado);
                }
            }
        } catch (ClassNotFoundException e) {
            System.out.println("Controlador no Encontrado: " + e);
        } catch (Exception e) {
            System.out.println("Error de Conexión: " + e);
        }
    }

    public void mostrarResultados(ResultSet r) throws SQLException {
        txtId.setText(r.getString("IdCategoria"));
        txtNombre.setText(r.getString("Nombre"));
        txtDescripcion.setText(r.getString("Descripcion"));
    }

    public void IrPrimero() {
        try {
            resultado.first();
            mostrarResultados(resultado);
        } catch (Exception e) {
            System.out.println("Error IrPrimero: " + e);
        }
    }

    public void IrAnterior() {
        try {
            if (!resultado.previous())
                resultado.first();
            mostrarResultados(resultado);
        } catch (Exception e) {
            System.out.println("Error IrAnterior: " + e);
        }
    }

    public void IrSiguiente() {
        try {
            if (!resultado.next())
                resultado.last();
            mostrarResultados(resultado);
        } catch (Exception e) {
            System.out.println("Error IrSiguiente: " + e);
        }
    }

    public void IrUltimo() {
        try {
            resultado.last();
            mostrarResultados(resultado);
        } catch (Exception e) {
            System.out.println("Error IrUltimo: " + e);
        }
    }

    // Métodos de operaciones
    public void IrInsertar() {
        try {
            String var2 = txtNombre.getText();
            String var3 = txtDescripcion.getText();

            PreparedStatement ps = conexion.prepareStatement(
                "INSERT INTO Categorias (Nombre, Descripcion) VALUES (?, ?)",
                Statement.RETURN_GENERATED_KEYS
            );
            ps.setString(1, var2);
            ps.setString(2, var3);

            int cantidad = ps.executeUpdate();

            if (cantidad > 0) {
                ResultSet claves = ps.getGeneratedKeys();
                if (claves.next()) {
                    int idGenerado = claves.getInt(1);
                    txtId.setText(String.valueOf(idGenerado));
                    System.out.println("ID generado: " + idGenerado);
                }
            }

            ps.close();

            // Refresca el resultado y ubica en el nuevo registro (si deseas)
            IrActualizar();

        } catch (Exception e) {
            System.out.println("Error Insertar: " + e);
        }
    }



    public void IrModificar() {
        try {
            String id = txtId.getText();
            String nombre = txtNombre.getText();
            String descripcion = txtDescripcion.getText();
            sentencia.executeUpdate("UPDATE Categorias SET " +
                    "Nombre='" + nombre + "', " +
                    "Descripcion='" + descripcion + "' " +
                    "WHERE IdCategoria=" + id);
        } catch (Exception e) {
            System.out.println("Error Modificar: " + e);
        }
    }

    public void IrEliminar() {
        try {
            String id = txtId.getText();
            sentencia.executeUpdate("DELETE FROM Categorias WHERE IdCategoria=" + id);
        } catch (Exception e) {
            System.out.println("Error Eliminar: " + e);
        }
    }

    public void IrActualizar() {
        try {
            sentencia.execute("SELECT * FROM Categorias");
            resultado = sentencia.getResultSet();
            if (resultado != null && resultado.first()) {
                mostrarResultados(resultado);
            }
        } catch (Exception e) {
            System.out.println("Error Actualizar: " + e);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            Ventana miVentana = new Ventana("Navegador de Categorías");
            miVentana.pack();
            miVentana.setVisible(true);
        });
    }
}