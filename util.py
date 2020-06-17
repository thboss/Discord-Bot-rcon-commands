class RconError(ValueError):
    pass

def strip_rcon_logline(response):
    lines = response.splitlines()
    if len(lines) >= 1:
        last_line = lines[len(lines) - 1]
        if 'rcon from' in last_line:
            return '\n'.join(lines[:len(lines) - 1])
    return response

def send_rcon_command(host, port, rcon_password, command,
                      raise_errors=False, num_retries=3, timeout=3.0):
    from valve.rcon import (RCON, RCONCommunicationError, RCONAuthenticationError)

    attempts = 0
    while attempts < num_retries:
        attempts += 1
        try:
            with RCON((host, port), rcon_password, timeout=timeout) as rcon:
                response = rcon(command)
                return strip_rcon_logline(response)

        except ConnectionRefusedError:
            return None

        except KeyError:
            raise RconError('Incorrect rcon password')

        except (RCONCommunicationError, RCONAuthenticationError) as e:
            if attempts >= num_retries:
                if raise_errors:
                    raise RconError(str(e))
                else:
                    return None
