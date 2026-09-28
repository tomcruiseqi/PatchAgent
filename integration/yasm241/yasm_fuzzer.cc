#include <sys/wait.h>
#include <unistd.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

extern "C" int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    char path[] = "/tmp/yasm-poc-XXXXXX";
    int input = mkstemp(path);
    if (input < 0)
        return 0;
    size_t written = 0;
    while (written < size) {
        ssize_t n = write(input, data + written, size - written);
        if (n <= 0)
            break;
        written += static_cast<size_t>(n);
    }
    close(input);

    int diagnostics[2];
    if (pipe(diagnostics) != 0) {
        unlink(path);
        return 0;
    }
    pid_t child = fork();
    if (child < 0) {
        close(diagnostics[0]);
        close(diagnostics[1]);
        unlink(path);
        return 0;
    }
    if (child == 0) {
        close(diagnostics[0]);
        dup2(diagnostics[1], STDERR_FILENO);
        close(diagnostics[1]);
        execl("/out/yasm-bin", "yasm-bin", path, static_cast<char *>(nullptr));
        _exit(127);
    }
    close(diagnostics[1]);
    std::string output;
    char buffer[4096];
    ssize_t n;
    while ((n = read(diagnostics[0], buffer, sizeof(buffer))) > 0)
        output.append(buffer, static_cast<size_t>(n));
    close(diagnostics[0]);
    int status = 0;
    waitpid(child, &status, 0);
    unlink(path);

    if (output.find("ERROR: AddressSanitizer:") != std::string::npos ||
        output.find("ERROR: LeakSanitizer:") != std::string::npos) {
        fwrite(output.data(), 1, output.size(), stderr);
        _exit(1);
    }
    return 0;
}
