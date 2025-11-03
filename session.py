from instagrapi import Client, exceptions
import getpass
import sys

def main():
    cl = Client()

    try:
        username = input("👤 Usuario de Instagram: ").strip()
        if not username:
            print("Usuario obligatorio.")
            sys.exit(1)

        password = getpass.getpass("🔑 Contraseña: ")

        print("🔐 Intentando iniciar sesión...")
        cl.login(username, password)
    except exceptions.TwoFactorRequired:
        code = input("📱 Cuenta con 2FA. Ingresá el código recibido: ").strip()
        try:
            cl.two_factor_login(username, password, code)
        except Exception as e:
            print("❌ Error en 2FA:", e)
            sys.exit(1)
    except exceptions.ChallengeRequired as e:
        print("⚠️ Instagram solicita verificación adicional (challenge). Revisa la app oficial o el correo).")
        print("Detalles:", e)
        sys.exit(1)
    except Exception as e:
        print("❌ Error al iniciar sesión:", e)
        sys.exit(1)

    # Si llegamos aquí, el login fue exitoso
    try:
        cl.dump_settings("session.json")
        print("✅ Sesión guardada correctamente en 'session.json'")
    except Exception as e:
        print("❌ Error al guardar session.json:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

