# Introducción a la Blockchain

Una blockchain es esencialmente una cadena de bloques donde cada bloque contiene datos, un hash del bloque anterior, un nonce (número utilizado una sola vez) y un hash actual. La integridad de la blockchain se mantiene mediante un proceso llamado "minería", que implica resolver problemas complejos de prueba de trabajo (Proof of Work, PoW).

# Definiendo las Clases Principales

Para nuestra implementación básica, necesitamos definir varias clases esenciales: Block, Blockchain, Transaction y Node.

**Clase Block**

La clase Block representa un bloque en la blockchain. Contiene información como el índice del bloque, las transacciones, la marca de tiempo, el hash del bloque anterior, el nonce y el hash actual del bloque.

**Clase Blockchain**

La clase Blockchain maneja la cadena de bloques. Inicializa con un bloque génesis y tiene métodos para añadir bloques y verificar la integridad de la cadena. También maneja las transacciones pendientes, que se almacenan en una pila (estructura LIFO - Last In, First Out).

**Clase Transaction**

La clase Transaction representa una transacción en la blockchain.

**Clase Node**

La clase Node es responsable de crear transacciones y añadirlas a la pila de transacciones pendientes.

# Ejecución y Prueba

Para probar nuestra implementación, creamos una función main que inicializa la blockchain y el nodo, crea varias transacciones, y mina un nuevo bloque con esas transacciones.

Este código creará transacciones, las añadirá a la pila de transacciones pendientes, minará un nuevo bloque con esas transacciones, verificará la integridad de la cadena y mostrará la información de cada bloque en la consola.

# Conclusión

Hemos construido una blockchain básica en Python que puede ser la base para futuras expansiones y mejoras. Algunas posibles funcionalidades adicionales que podrías añadir incluyen:

Validación de Transacciones: Asegurarse de que las transacciones sean válidas antes de añadirlas a la blockchain.
Red P2P: Implementar una red peer-to-peer para que múltiples nodos puedan interactuar entre sí.
Contratos Inteligentes: Añadir soporte para contratos inteligentes que ejecuten código automáticamente en la blockchain.
